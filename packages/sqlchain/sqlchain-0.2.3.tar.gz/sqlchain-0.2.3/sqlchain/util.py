#
# Common sqlchain support utils 
#
import os, sys, socket, pwd, time, hashlib, json, threading, re, glob, urllib2

from Queue import Queue
from backports.functools_lru_cache import lru_cache
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from struct import pack, unpack, unpack_from
from datetime import datetime
from hashlib import sha256

tidylog = threading.Lock()

# cannot change these without first updating existing table schema and data
# these are set to reasonable values for now - to increase, alter trxs.block_id or outputs.id column widths
# and update data eg. update trxs set block_id=block_id/OLD_MAX*NEW_MAX + block_id%OLD_MAX
MAX_TX_BLK = 10000  # allows 9,999,999 blocks with decimal(11)
MAX_IO_TX = 4096    # allows 37 bit out_id value, (5 byte hash >> 3)*4096 in decimal(16), 7 bytes in blobs
BLOB_SPLIT_SIZE = int(5e9) # size limit for split blobs, approx. as may extend past if tx on boundary
S3_BLK_SIZE = 4096 # s3 block size for caching

b58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

class dotdict(dict):
     """dot.notation for more concise globals access on dict"""
     def __getattr__(self, attr):
         return self.get(attr)
     __setattr__= dict.__setitem__
     __delattr__= dict.__delitem__

# address support stuff
def is_address(addr):
    try:
        n = 0
        for c in addr:
            n = n * 58 + b58.index(c)
        btc = ('%%0%dx' % (25 << 1) % n).decode('hex')[-25:]
        return btc[-4:] == sha256(sha256(btc[:-4]).digest()).digest()[:4]
    except Exception:
        return False
        
def mkpkh(pk):
    rmd = hashlib.new('ripemd160')
    rmd.update(sha256(pk).digest())
    return rmd.digest()

def addr2pkh(v):
    long_value = 0L
    for (i, c) in enumerate(v[::-1]):
        long_value += b58.find(c) * (58**i)
    result = ''
    while long_value >= 256:
        div, mod = divmod(long_value, 256)
        result = chr(mod) + result
        long_value = div
    result = chr(long_value) + result
    nPad = 0
    for c in v:
        if c == b58[0]: nPad += 1
        else: break
    result = chr(0)*nPad + result
    return result[1:-4]
    
def mkaddr(pkh, aid=None, p2sh=False):
    if pkh == '\0'*20 and aid==0:
        return '' # pkh==0 id==0, special case for null address when op_return or non-std script
    pad = ''
    an = chr((111 if sqc.testnet else 0) if (aid is None and not p2sh) or (aid is not None and aid%2==0) else (196 if sqc.testnet else 5)) + str(pkh)
    for c in an:
        if c == '\0': pad += '1'
        else: break
    num = long((an + sha256(sha256(an).digest()).digest()[0:4]).encode('hex'), 16)
    out = ''
    while num >= 58:
        num,m = divmod(num, 58)
        out = b58[m] + out
    return pad + b58[num] + out 

def addr2id(addr, cur=None, rtnPKH=False):
    pkh = addr2pkh(addr)
    addr_id, = unpack('<q', sha256(pkh).digest()[:5]+'\0'*3) 
    addr_id *= 2
    if addr[0] in '32': # encode P2SH as odd id, P2PKH as even id
        addr_id += 1
    if cur:
        cur.execute("select id from address where id>=%s and id<%s+32 and addr=%s limit 1;", (addr_id,addr_id,pkh))
        row = cur.fetchone()
        return row[0] if row else None
    return addr_id,pkh if rtnPKH else addr_id

# script support stuff
def mkSPK(addr, addr_id):
    return ('\x19','\x76\xa9\x14%s\x88\xac'%addr) if addr_id % 2 == 0 else ('\x17','\xa9\x14%s\x87'%addr)
    
def decodeScriptPK(data):
    if len(data) > 1:
        if len(data) == 25 and data[:3] == '\x76\xa9\x14' and data[23:25] == '\x88\xac': # P2PKH
            return { 'type':'p2pkh', 'data':'', 'addr':mkaddr(data[3:23]) };
        if len(data) == 23 and data[:2] == '\xa9\x14' and data[22] == '\x87': # P2SH
            return { 'type':'p2sh', 'data':'', 'addr':mkaddr(data[2:22],p2sh=True)};
        if len(data) == 67 and data[0] == '\x41' and data[66] == '\xac': # P2PK
            return { 'type':'p2pk', 'data':data, 'addr':mkaddr(mkpkh(data[1:66])) };
        if len(data) >= 35 and data[0] == '\x21' and data[34] == '\xac': # P2PK (compressed key)
            return { 'type':'p2pk', 'data':data, 'addr':mkaddr(mkpkh(data[1:34])) };
        if len(data) >= 38 and data[:6] == '\x6a\x24\aa\21\a9\ed': # witness commitment
            return { 'type':'witness', 'hash':data[6:38], 'data':data[38:] };
        if len(data) <= 41 and data[0] == '\x6a': # OP_RETURN
            return { 'type':'null', 'data':data };
    return { 'type':'other', 'data':data } # other, non-std
    
OpCodes = { '\x4F':'OP_1NEGATE', '\x61':'OP_NOP', '\x63':'OP_IF', '\x64':'OP_NOTIF', '\x67':'OP_ELSE', '\x68':'OP_ENDIF', 
            '\x69':'OP_VERIFY', '\x6A':'OP_RETURN', '\x6B':'OP_TOALTSTACK', '\x6C':'OP_FROMALTSTACK', '\x6D':'OP_2DROP', '\x6E':'OP_2DUP', 
            '\x6F':'OP_3DUP', '\x70':'OP_2OVER', '\x71':'OP_2ROT', '\x72':'OP_2SWAP','\x73':'OP_IFDUP', '\x74':'OP_DEPTH', '\x75':'OP_DROP', 
            '\x76':'OP_DUP', '\x77':'OP_NIP', '\x78':'OP_OVER', '\x79':'OP_PICK', '\x7A':'OP_ROLL', '\x7B':'OP_ROT', '\x7C':'OP_SWAP', 
            '\x7D':'OP_TUCK',  '\x7E':'OP_CAT', '\x7F':'OP_SUBSTR', '\x80':'OP_LEFT', '\x81':'OP_RIGHT', '\x82':'OP_SIZE', '\x83':'OP_INVERT', 
            '\x84':'OP_AND', '\x85':'OP_OR', '\x86':'OP_XOR', '\x87':'OP_EQUAL', '\x88':'OP_EQUALVERIFY', '\x8B':'OP_1ADD', '\x8C':'OP_1SUB', 
            '\x8D':'OP_2MUL', '\x8E':'OP_2DIV', '\x8F':'OP_NEGATE', '\x90':'OP_ABS', '\x91':'OP_NOT', '\x92':'OP_0NOTEQUAL', '\x93':'OP_ADD',
            '\x94':'OP_SUB', '\x95':'OP_MUL', '\x96':'OP_DIV', '\x97':'OP_MOD', '\x98':'OP_LSHIFT', '\x99':'OP_RSHIFT', '\x9A':'OP_BOOLAND', 
            '\x9B':'OP_BOOLOR', '\x9C':'OP_NUMEQUAL', '\x9D':'OP_NUMEQUALVERIFY', '\x9E':'OP_NUMNOTEQUAL', '\x9F':'OP_LESSTHAN', 
            '\xA0':'OP_GREATERTHAN', '\xA1':'OP_LESSTHANOREQUAL', '\xA2':'OP_GREATERTHANOREQUAL', '\xA3':'OP_MIN', '\xA4':'OP_MAX', 
            '\xA5':'OP_WITHIN', '\xA6':'OP_RIPEMD160', '\xA7':'OP_SHA1', '\xA8':'OP_SHA256', '\xA9':'OP_HASH160', '\xAA':'OP_HASH256', 
            '\xAB':'OP_CODESEPARATOR ', '\xAC':'OP_CHECKSIG', '\xAD':'OP_CHECKSIGVERIFY', '\xAE':'OP_CHECKMULTISIG', '\xAF':'OP_CHECKMULTISIGVERIFY',
            '\xFD':'OP_PUBKEYHASH', '\xFE':'OP_PUBKEY', '\xFF':'OP_INVALIDOPCODE', '\x50':'OP_RESERVED', '\x62':'OP_VER', '\x65':'OP_VERIF', 
            '\x66':'OP_VERNOTIF', '\x89':'OP_RESERVED1', '\x8A':'OP_RESERVED2' }
    
def mkOpCodeStr(data, sepOP=' ', sepPUSH='\n'):
    ops,pos = '',0
    while pos < len(data):
        if data[pos] == 0:
            ops += 'OP_0'+sepOP
        elif data[pos] <= '\x4C':
            sz, = unpack('<B', data[pos])
            ops += data[pos+1:pos+1+sz].encode('hex')+sepPUSH
            pos += sz
        elif data[pos] == '\x4C':
            sz, = unpack('<B', data[pos+1:])
            ops += data[pos+2:pos+2+sz].encode('hex')+sepPUSH
            pos += sz
        elif data[pos] == '\x4D':
            sz, = unpack('<H', data[pos+1:])
            ops += data[pos+2:pos+2+sz].encode('hex')+sepPUSH
            pos += sz
        elif data[pos] == '\x4E':
            sz, = unpack('<I', data[pos+1:])
            ops += data[pos+2:pos+2+sz].encode('hex')+sepPUSH
            pos += sz
        elif data[pos] >= '\x50' and data[pos] <= '\x60':
            ops += 'OP_'+str(int(data[pos]))+sepOP
        elif data[pos] >= '\xB0' and data[pos] <= '\xB9':
            ops += 'OP_NOP'+str(int(data[pos])+1)+sepOP
        else: 
            ops += OpCodes[data[pos]]+sepOP
        pos += 1
    return ops

def decodeVarInt(v):
    if v[0] <= '\xfc':
        return unpack('<B', v[0])[0],1
    if v[0] == '\xfd':
        return unpack('<H', v[1:3])[0],3
    if v[0] == '\xfe':
        return unpack('<I', v[1:5])[0],5
    return unpack('<Q', v[1:9])[0],9
    
def encodeVarInt(v):
    if v <= 252:
        return pack('<B', v)
    if v < 2**16:
        return '\xfd' + pack('<H', v)
    if v < 2**32:
        return '\xfe' + pack('<I', v)
    return '\xff' + pack('<Q', v)

# sqlchain ids support stuff
def txh2id(txh):
    return ( unpack('<q', txh[:5]+'\0'*3)[0] >> 3 )
    
addr_lock = threading.Lock()

def insertAddress(cur, addr):
    addr_id,pkh = addr2id(addr, rtnPKH=True)
    start_id = addr_id
    with addr_lock:
        while True:
            cur.execute("select addr from address where id=%s", (addr_id,))
            row = cur.fetchone()
            if row == None:
                cur.execute("insert into address (id,addr) values(%s,%s)", (addr_id, pkh))
                return addr_id
            elif str(row[0]) == str(pkh):
                return addr_id
            addr_id += 2
        
def findTx(cur, txhash, mkNew=False, limit=32):
    tx_id = txh2id(txhash)
    limit_id = tx_id+limit
    start_id = tx_id
    while True:
        cur.execute("select hash from trxs where id=%s", (tx_id,))
        row = cur.fetchone()
        if row == None:
            if mkNew:
                return (tx_id,False)
            return None
        if str(row[0]) == str(txhash):
            return (tx_id,True) if mkNew else tx_id
        if tx_id > limit_id:
            logts("*** Tx Id limit exceeded %s ***" % txhash)
            return (None,False) if mkNew else None
        tx_id += 1

# blob and header file support stuff 
def puthdr(blk, hdr, path='/var/data'):
    with open(path+'/hdrs.dat', 'r+b') as f:
        f.seek(blk*80)
        f.write(hdr)
        f.flush()
        
def gethdr(blk, var=None, path='/var/data'):
    with open(path+'/hdrs.dat', 'rb') as f:
        f.seek(blk*80)
        data = f.read(80)
    hdr = dict(zip(['version','previousblockhash','merkleroot', 'time', 'bits', 'nonce'], unpack_from('<I32s32s3I', data)))
    return hdr if var == None else hdr[var] if var != 'raw' else data

def getChunk(chunk, path='/var/data'):
    with open(path+'/hdrs.dat', 'rb') as f:
        f.seek(chunk*80*2016)
        return f.read(80*2016)
        
def bits2diff(bits):
    return (0x00ffff * 2**(8*(0x1d - 3)) / float((bits&0xFFFFFF) * 2**(8*((bits>>24) - 3))))
    
def getBlobHdr(pos, path='/var/data'):
    buf = readBlob(int(pos), 13, path) 
    bits = [ (1,'B',0), (1,'B',0), (2,'H',0), (4,'I',1), (4,'I',0) ]  # ins,outs,tx size,version,locktime
    out,mask = [1],0x80 
    for sz,typ,default in bits:
        if ord(buf[0])&mask:
            out.append(unpack('<'+typ, buf[out[0]:out[0]+sz])[0])
            out[0] += sz
        else:
            out.append(default)
        mask >>= 1
    out.append( ord(buf[0])&0x04 == 0 )  # stdSeq
    out.append( ord(buf[0])&0x02 != 0 )  # nosigs
    out.append( ord(buf[0])&0x01 != 0 )  # segwit
    return out # out[0] is hdr size

def mkBlobHdr(ins, outs, tx, stdSeq, nosigs, segwit):
    flags,hdr = 0,''
    sz = tx['size']
    if ins >= 0xC0:
        flags |= 0x80
        hdr += pack('<B', ins & 0xFF)
        ins = 0xC0|(ins>>8)
    if outs >= 0xC0:
        flags |= 0x40
        hdr += pack('<B', outs & 0xFF)
        outs = 0xC0|(outs>>8)
    if sz >= 0xFF00:
        flags |= 0x20
        hdr += pack('<H', sz & 0xFFFF)
        sz = 0xFF00|(sz>>16)
    if tx['version'] != 1:
        flags |= 0x10
        hdr += pack('<I', tx['version'])
    if tx['locktime'] != 0:
        flags |= 0x08
        hdr += pack('<I', tx['locktime'])
    if not stdSeq:
        flags |= 0x04  
    if nosigs:
        flags |= 0x02
    if segwit:
        flags |= 0x01
    # max hdr = 13 bytes but most will be only 1 flag byte
    return ins,outs,sz,pack('<B', flags) + hdr

blob_lock = threading.Lock()
    
def insertBlob(data, path='/var/data'):
    if len(data) == 0:
        return 0
    fn = '/blobs.dat'
    pos,off = (0,2)
    with blob_lock:
        if not os.path.exists(path+fn): # support split blobs
            try:
                fn = '/blobs.%d.dat' % (insertBlob.nextpos//BLOB_SPLIT_SIZE,)
            except AttributeError:
                n = 0
                for f in glob.glob(path+'/blobs.*[0-9].dat'): # should happen only once as init
                    n = max(n, int(re.findall('\d+', f)[0]))
                pos = os.path.getsize(path+'/blobs.%d.dat' % n) if os.path.exists(path+'/blobs.%d.dat' % n) else 0
                insertBlob.nextpos =  n*BLOB_SPLIT_SIZE + pos
                fn = '/blobs.%d.dat' % (insertBlob.nextpos//BLOB_SPLIT_SIZE,) # advances file number when pos > split size
            pos,off = (insertBlob.nextpos % BLOB_SPLIT_SIZE, 0)
            rtnpos = insertBlob.nextpos
            insertBlob.nextpos += len(data)
        with open(path+fn, 'r+b' if os.path.exists(path+fn) else 'wb') as blob:
            blob.seek(pos,off)
            newpos = blob.tell()
            blob.write(data)
        return rtnpos if 'rtnpos' in locals() else newpos


def readBlob(pos, sz, path='/var/data'):
    if sz == 0:
        return ''
    fn = '/blobs.dat'
    if not os.path.exists(path+fn): # support split blobs
        fn = '/blobs.%d.dat' % (pos//BLOB_SPLIT_SIZE)
        pos = pos % BLOB_SPLIT_SIZE
    if not os.path.exists(path+fn): # file missing, try s3 if available
        if sqc and 'cfg' in sqc and 's3' in sqc.cfg:
            return s3get(sqc.cfg['s3']+fn, pos, sz)
        return '\0'*sz  # data missing, return zeros as null data (not ideal)
    with open(path+fn, 'rb') as blob:
        blob.seek(pos)
        return blob.read(sz)
        
def s3get(blob, pos, sz):
    data = ''
    for blk in range(pos // S3_BLK_SIZE, (pos+sz) // S3_BLK_SIZE + 1):
        data += s3blk(blob, blk)
    return data[ pos % S3_BLK_SIZE : pos % S3_BLK_SIZE + sz ]
    
@lru_cache(maxsize=512)
def s3blk(blob, blk):
    log( "S3 REQ: %s %d" % (blob,blk) )
    req = urllib2.Request(blob)
    req.add_header('Range', 'bytes=%d-%d' % (blk*S3_BLK_SIZE,(blk+1)*S3_BLK_SIZE-1))
    resp = urllib2.urlopen(req)
    return resp.read(S3_BLK_SIZE)
    
def getBlobsSize(path='/var/data'):
    sz = 0
    for f in glob.glob(path+'/blobs*.dat'):
        sz += os.stat(f).st_size 
    return sz

# cfg file handling stuff
def loadcfg(cfg):
    cfgpath = sys.argv[-1] if len(sys.argv) > 1 and sys.argv[-1][0] != '-' else os.path.basename(sys.argv[0])+'.cfg'
    try:
        with open(cfgpath) as json_file:
            cfg.update(json.load(json_file))
    except IOError:
        logts('No cfg file.')
    finally:
        cfg['debug'] = False

def savecfg(cfg):
    cfgpath = sys.argv[-1] if len(sys.argv) > 1 and sys.argv[-1][0] != '-' else os.path.basename(sys.argv[0])+'.cfg'
    try:
        with open(cfgpath, 'w') as json_file:
            json.dump(cfg, json_file, indent=2)
    except IOError:
        logts('Cannot save cfg file')

def logts(msg):
    tidylog.acquire()
    print datetime.now().strftime('%d-%m-%Y %H:%M:%S'), msg
    sys.stdout.flush() 
    tidylog.release()
    
def log(msg):
    tidylog.acquire()
    print msg
    sys.stdout.flush()
    tidylog.release()

def drop2user(cfg, chown=False):
    if ('user' in cfg) and (cfg['user'] != '') and (os.getuid() == 0):
        pw = pwd.getpwnam(cfg['user'])
        if chown:
            logfile = cfg['log'] if 'log' in cfg else sys.argv[0]+'.log'
            pidfile = cfg['pid'] if 'pid' in cfg else sys.argv[0]+'.pid'
            if os.path.exists(logfile):
                os.chown(logfile, pw.pw_uid, pw.pw_gid)
            if os.path.exists(pidfile):
                os.chown(pidfile, pw.pw_uid, pw.pw_gid)
        os.setgroups([])
        os.setgid(pw.pw_gid)
        os.setuid(pw.pw_uid)
        os.umask(0022) 
        log('Dropped to user %s' % cfg['user'])

def getssl(cfg):
    if not ('ssl' in cfg) or (cfg['ssl'] == ''):
        return {}

    logts("Loading SSL certificate chain.")
    if sys.version_info < (2,7,9):
        log("*** Warning: Upgrade to Python 2.7.9 for better SSL security! ***")
        cert = { 'certfile':cfg['ssl'] }                                                        # ssl = key+cert in one file, or cert only
        cert.update({ 'keyfile':cfg['key'] } if ('key' in cfg) and (cfg['key'] != '') else {})  # with key in 2nd file
        return cert
    
    from gevent.ssl import SSLContext, PROTOCOL_SSLv23
    context = SSLContext(PROTOCOL_SSLv23)
    context.load_cert_chain(cfg['ssl'], cfg['key'] if ('key' in cfg) and (cfg['key'] != '') else None)
    return { 'ssl_context': context }

rpc_lock = threading.Lock()

class rpcPool(object):
    def __init__(self, cfg, size=4, timeout=30):
        self.url = cfg['rpc']
        self.timeout = timeout
        #self.connQ = blockQ = Queue(size)
        #for n in range(size):
        #    self.connQ.put(AuthServiceProxy(cfg['rpc'], None, timeout, None))
            
    def __getattr__(self, name):
        if name.startswith('__') and name.endswith('__'):
            raise AttributeError
        rpc_lock.acquire()
        self.name = name
        return self
        
    def __call__(self, *args):
        name = self.name
        rpc_lock.release()
        rpc_obj = AuthServiceProxy(self.url, None, self.timeout, None)
        #rpc_obj = self.connQ.get()
        while True:
            try:
                result = rpc_obj.__getattr__(name)(*args)
                break
            except JSONRPCException as e:
                if e.code == -5:
                    return None
            except Exception as e:
                log( 'RPC Error ' + str(e) + ' (retrying)' )
                print "===>", name, args
                #if sqc and 'done' in sqc and sqc.done.isSet():
                #    raise socket.error # shutdown, otherwise hung daemon
                rpc_obj = AuthServiceProxy(self.url, None, self.timeout, None) # maybe broken, make new connection
                time.sleep(3) # slow down, in case gone away
                pass
        #self.connQ.put(rpc_obj)
        return result
            
                
            
            
