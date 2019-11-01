from Cryptodome.Signature import pss
from Cryptodome.Hash import SHA512
from Cryptodome.PublicKey import RSA
from Cryptodome import Random
from Cryptodome.IO import PEM

def sign(fileIn, privKeyPath, signatureOut=None, return_signature=False):
    if not signatureOut:
        signatureOut = fileIn + '.sign'
    
    with open(fileIn, 'rb') as f:
        data = f.read()
    
    with open(privKeyPath, 'rb') as f:
        privKey = RSA.import_key(f.read())
    
    dataHash = SHA512.new(data)
    signature = pss.new(privKey).sign(dataHash)
    if return_signature:
        return signature
    with open(signatureOut, 'w') as f:
        f.write(PEM.encode(signature, 'PKCS1-PSS SIGNATURE'))


def verify(fileIn, signaturePath, pubKeyPath):
    with open(fileIn, 'rb') as f:
        data = f.read()

    with open(signaturePath, 'r') as f:
        signature = PEM.decode(f.read())[0]

    with open(pubKeyPath, 'rb') as f:
        pubKey = RSA.import_key(f.read())

    fileHash = SHA512.new(data)
    verifier = pss.new(pubKey)

    try:
        verifier.verify(fileHash, signature)
        return True
    except (ValueError, TypeError):
        return False
