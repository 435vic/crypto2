import os
import struct
from io import BytesIO
from sys import argv
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Hash.SHA256 import SHA256Hash
from Cryptodome import Random
from Cryptodome.Util.Padding import pad
from tqdm import tqdm
from signature import sign, verify
from fileformat import write_crypt2

IV_BLOCK_SIZE = 16

#region Functions


def encrypt(key, fileIn, rsa=False, signature_privKey=None, chunksize=64 * 1024):
    key = SHA256Hash(key).digest()
    iv = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(fileIn)
    encfilesize = filesize + (AES.block_size - filesize % AES.block_size) + 24
    if rsa:
        encfilesize -= 24
    pbar = tqdm(desc='Encrypting', total=encfilesize, unit='Bytes', unit_scale=1)
    out = BytesIO()

    with open(fileIn, 'rb') as infile:
        with out as outfile:
            if not rsa:
                outfile.write(struct.pack('<Q', filesize))
                outfile.write(iv)
                pbar.update(24)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % IV_BLOCK_SIZE != 0:
                    chunk = pad(chunk, IV_BLOCK_SIZE)

                enc_chunk = encryptor.encrypt(chunk)
                outfile.write(enc_chunk)
                pbar.update(len(enc_chunk))
            
            encrypted = out.getvalue()
    
    if rsa:
        if signature_privKey:
            signature = sign(fileIn, signature_privkey, return_signature=True)
            return encrypted, iv, filesize, signature

    if signature_privKey:
        signature = sign(fileIn, signature_privkey, return_signature=True)
        write_crypt2(fileIn + '.crypt2', encrypted, iv, filesize, signature)
        return

    with open(fileIn + '.crypt', 'wb') as fout:
        fout.write(encrypted)
    
    pbar.close()
    _tmp = input('Press enter to continue...')


def decrypt(key, fileIn, fileOut=None, chunksize=24 * 1024):
    key = SHA256Hash(key).digest()
    if not fileOut:
        fileOut = os.path.splitext(fileIn)[0]

    with open(fileIn, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(IV_BLOCK_SIZE)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        pbar = tqdm(desc='Decrypting', total=origsize - 24, unit='B', unit_scale=1)

        with open(fileOut, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))
                pbar.update(chunksize)

            outfile.truncate(origsize)
    
    pbar.close()
    _tmp = input('Press enter to continue...')

#endregion Functions

def main():
    pass

if __name__ == '__main__':
    main()
