import pickle
import struct

formatVersion = '1.0'

class VersionError(Exception):
    pass

# def read_crypt2(filename):
#     with open(filename) as fin:
#         pickled = struct.unpack('<H', fin.read(struct.calcsize('<H')))[0]
#         metadata = pickle.unpack(pickled)
#         if metadata.version is not formatVersion:
#             raise VersionError('Version {} does not match {}'.format(formatVersion, metadata.version))
#         file = struct.unpack('<Q', fin.read(struct.calcsize('<Q')))[0]
#         aesKey = struct.unpack('<L', fin.read(struct.calcsize('<L')))[0]
#         if metadata.rsa:
#             rsaKey = struct.unpack('<L', fin.read(struct.calcsize('<L')))[0]


# def write_crypt2(rsap=False, compressedp=False, file, aesKey, rsaKey=None, filename):
#     picklobj = {
#         rsa: rsap,
#         compressed: compressedp, #TODO
#         version: formatVersion
#     }
#     pickled = pickled.dunps(picklobj)
#     with open(filename, 'wb')as out:
#         out.write('crypt2ff'.encode('utf-8'))
#         out.write(struct.pack('<H', len(pickled)))
#         out.write(pickled)
#         out.write(struct.pack('<Q',len(file))) 
#         out.write(file)
#         out.write(struct.pack('<L',len(aesKey))) 
#         out.write(aesKey)
#         if rsaKey:
#             out.write(struct.pack('<L',len(rsaKey)))
#         if rsaKey:
#             out.write(rsaKey)

def write_crypt2(filename, encrypted, iv, origsize, signature, rsaKey=None):
    # signature of original, unencrypted data
    metadata = {
        'rsa': True if rsaKey else False,
        'version': formatVersion
    }
    pickled = pickle.dumps()
    with open(filename, 'wb') as fout:
        out.write(b'crypt2ff') # File signature
        out.write(struct.pack('<H', len(pickled))) # Length of pickled metadata
        out.write(struct.pack('<Q', origsize)) # Length of original file
        out.write(struct.pack('<Q', len(encrypted))) # Length of encrypted file
        out.write(iv) # Initialization Vector (required for AES-CBC)
        out.write(struct.pack('<H', len(signature))) # length of signature
        if rsaKey:
            out.write(struct.pack('<L',len(rsaKey))) # length of rsa key
            out.write(rsaKey) # rsa key
        out.write(pickled)
        out.write(encrypted)
        out.write(signature)
        
