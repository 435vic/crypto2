from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import PKCS1_OAEP
import aes
from Cryptodome.IO import PEM
from os.path import splitext

def generate(bits, keysFolder):
    keys = RSA.generate(bits)
    priv = keys.export_key()
    pub = keys.publickey().export_key()
    with open('%s/public.pem' % keysFolder, 'wb') as f:
        f.write(pub)
    
    with open('%s/private.pem' % keysFolder, 'wb') as f:
        f.write(priv)

def encrypt(pubKeyPath, filename, encfilename=None, keyfilename=None, chunksize=64*1024):
    if not encfilename:
        encfilename = filename + '.crypt'
    if not keyfilename:
        keyfilename = filename + '.key'
    
    aeskey = get_random_bytes(32)
    pubKey = RSA.import_key(pubKeyPath)
    aes.encrypt(aeskey, filename, encfilename, chunksize)
    rsa_enc = PKCS1_OAEP.new(pubKey)
    encKey = rsa_enc.encrypt(aeskey)
    PEMKey = PEM.encode(encKey, 'ENCRYPTED KEY')
    with open(keyfilename, 'wb') as out:
        out.write(PEMKey)

def decrypt(privKeyPath, encfilename, keyfilename, outfilename=None, chunksize=24*1024):
    if not outfilename:
        outfilename = splitext(outfilename)

    privKey = RSA.import_key(privKeyPath)
    with open(keyfilename, 'rb') as f:
        encKey = PEM.decode(f.read())[0]
    
    rsa_dec = PKCS1_OAEP.new(privKey)
    key = rsa_dec.decrypt(encKey)
    aes.decrypt(key, encfilename, outfilename, chunksize)

