import os
import struct
from sys import argv
from Cryptodome.Cipher import AES
from Cryptodome.Hash.SHA256 import SHA256Hash
from Cryptodome import Random
from Cryptodome.Util.Padding import pad

IV_BLOCK_SIZE = 16

#region Functions


def encrypt(key, fileIn, fileOut=None, chunksize=64 * 1024):
    key = SHA256Hash(key).digest()
    if not fileOut:
        fileOut = fileIn + '.crypt'

    iv = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(fileIn)

    with open(fileIn, 'rb') as infile:
        with open(fileOut, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % IV_BLOCK_SIZE != 0:
                    chunk = pad(chunk, IV_BLOCK_SIZE)

                outfile.write(encryptor.encrypt(chunk))


def decrypt(key, fileIn, fileOut=None, chunksize=24 * 1024):
    key = SHA256Hash(key).digest()
    if not fileOut:
        fileOut = os.path.splitext(fileIn)[0]

    with open(fileIn, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(IV_BLOCK_SIZE)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(fileOut, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)

#endregion Functions

def main():
    pass

if __name__ == '__main__':
    main()
