from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import PKCS1_OAEP
import aes
from fileformat import write_crypt2
from Cryptodome.IO import PEM
from os.path import splitext


def generate(bits, keysFolder):
    keys = RSA.generate(bits)
    priv = keys.export_key()
    pub = keys.publickey().export_key()
    with open('%s/rsa.pub' % keysFolder, 'wb') as f:
        f.write(pub)

    with open('%s/rsa' % keysFolder, 'wb') as f:
        f.write(priv)


def encrypt(pubKeyPath, privKeyPath, filename, keyfilename=None, chunksize=64*1024):
    aeskey = get_random_bytes(32)
    with open(pubKeyPath, 'rb') as f:
        pubKey = RSA.import_key(f.read())

    with open(privKeyPath, 'rb') as f:
        privKey = RSA.import_key(f.read())

    rsa_enc = PKCS1_OAEP.new(pubKey)
    encKey = rsa_enc.encrypt(aeskey)
    
    encrypted, iv, origsize, signature = aes.encrypt(aeskey, filename, encfilename, privKeyPath, chunksize)
    write_crypt2(filename + '.crypt2', encrypted, iv, origsize, signature, rsaKey=encKey)


def decrypt(privKeyPath, encfilename, keyfilename, outfilename=None, chunksize=24*1024):
    if not outfilename:
        outfilename = splitext(outfilename)

    with open(privKeyPath, 'rb') as f:
        privKey = RSA.import_key(f.read())

    with open(keyfilename, 'r') as f:
        encKey = PEM.decode(f.read())[0]

    rsa_dec = PKCS1_OAEP.new(privKey)
    key = rsa_dec.decrypt(encKey)
    aes.decrypt(key, encfilename, outfilename, chunksize)
