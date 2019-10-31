import pickle
import struct

formatVersion = '1.0'

class VersionError(Exception):
    pass

def read_crypt2(filename):
    with open(filename) as fin:
        pickled = struct.unpack('<H', fin.read(struct.calcsize('<H')))[0]
        metadata = pickle.unpack(pickled)
        if metadata.version is not formatVersion:
            raise VersionError('Version {} does not match {}'.format(formatVersion, metadata.version))
        file = struct.unpack('<Q', fin.read(struct.calcsize('<Q')))[0]
        aesKey = struct.unpack('<L', fin.read(struct.calcsize('<L')))[0]
        if metadata.rsa:
            rsaKey = struct.unpack('<L', fin.read(struct.calcsize('<L')))[0]


def write_crypt2(rsap=False, compressedp=False, file, aesKey, rsaKey=None, filename):
    picklobj = {
        rsa: rsap,
        compressed: compressedp, #TODO
        version: formatVersion
    }
    pickled = pickled.dunps(picklobj)
    with open(filename, 'wb')as out:
        out.write('crypt2ff'.encode('utf-8'))
        out.write(struct.pack('<H', len(pickled)))
        out.write(pickled)
        out.write(struct.pack('<Q',len(file))) 
        out.write(file)
        out.write(struct.pack('<L',len(aesKey))) 
        out.write(aesKey)
        if rsaKey:
            out.write(struct.pack('<L',len(rsaKey)))
        if rsaKey:
            out.write(rsaKey)
