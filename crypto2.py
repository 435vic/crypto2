#!/usr/bin/env python3
import argparse
import os
from getpass import getpass
from time import sleep
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilename, asksaveasfilename

import Cryptodome
from signature import sign, verify
import utils
import aes
import rsa
from utils import clear, title

cwd = os.getcwd

def AES():
    while True:
        title('AES Encryption / Decryption', fillchar='-')
        [print() for i in range(5)]
        print('Do you want to...')
        print('1. Encrypt a file')
        print('2. Decrypt a file')
        print('3. Exit')
        print('_' * utils.get_terminal_size()[0])
        print()
        action = input('>> ').lower()
        if action in ['1', 'encrypt', 'e']:
            title('AES Encryption / Decryption', fillchar='-')
            print(); print()
            print('Please select a file in the dialog box.')
            Tk().withdraw()
            filename = askopenfilename(initialdir=cwd, title='Choose a file to encrypt...')
            password = getpass('Enter password for file: ').encode('utf-8')
            print('Choose the name for the encrypted file.')
            outfilename = asksaveasfilename(initialdir=cwd, title='Choose the name for the encrypted file...')
            chunksize = input('Enter encryption chunksize: ') or 64 * 1024
            if chunksize:
                chunksize = int(chunksize)
            aes.encrypt(password, filename, outfilename, chunksize)

        elif action in ['2', 'decrypt', 'd']:
            title('AES Encryption / Decryption', fillchar='-')
            print(); print()
            print('Please select a file in the dialog box.')
            Tk().withdraw()
            filename = askopenfilename(initialdir=cwd, title='Choose a file to decrypt...')
            password = getpass('Enter password to decrpyt file: ').encode('utf-8')
            print('Choose the name for the output file.')
            outfilename = asksaveasfilename(initialdir=cwd, title='Choose the name for the decrypted file...')
            chunksize = input('Enter decryption chunksize: ') or 24 * 1024
            if chunksize:
                chunksize = int(chunksize)

            aes.decrypt(password, filename, outfilename, chunksize)

        elif action in ['3', 'exit', 'quit', 'q']:
            exit(0)

        else:
            clear()
            _tmp = input('That is not an action.')

def RSA(action):
    if action == '2':
        title('RSA keygen', fillchar='-')
        print(); print()
        print('Select directory for the keys.')
        Tk().withdraw()
        while True:
            outfolder = askdirectory(initialdir=cwd, title='Select directory to save keys in...')
            if not outfolder:
                print('Please choose a directory.')
            else:
                if not os.path.exists(outfolder):
                    os.makedirs(outfolder, exist_ok=True)
                break

        bits = int(input('Size of the key (default is 2048): ') or 2048)
        rsa.generate(bits, outfolder)

    elif action == '3':
        title('RSA Encryption / Decryption', fillchar='-')
        [print() for i in range(5)]
        print('Do you want to...')
        print('1. Encrypt a file')
        print('2. Decrypt a file')
        print('3. Exit')
        print('_' * utils.get_terminal_size()[0])
        print()
        action = input('>> ').lower()
        if action == '1':
            title('RSA Encryption / Decryption', fillchar='-')
            print(); print()
            print('Select a file to encrypt in the dialog box.')
            Tk().withdraw()
            filename = askopenfilename(initialdir=cwd, title='Choose a file to encrypt...')
            print(filename)
            print('Select the public key to encrypt the file with.')
            Tk().withdraw()
            keypath = askopenfilename(initialdir=cwd, title='Choose a public key...')
            print(keypath)
            print('Select the name for the encrypted file.')
            Tk().withdraw()
            outfile = asksaveasfilename(initialdir=cwd, title='Save as...')
            print('Select the name for the encrypted key.')
            Tk().withdraw()
            outkeyfile = asksaveasfilename(initialdir=cwd, title='Save as...')
            print(outfile)
            chunksize = input('Select chunksize (leave empty for default): ') or 64 * 1024
            rsa.encrypt(keypath, filename, outfile, outkeyfile, chunksize)
        
        elif action == '2':
            title('RSA Encryption / Decryption', fillchar='-')
            print(); print()
            print('Select a file to decrypt in the dialog box.')
            Tk().withdraw()
            filename = askopenfilename(initialdir=cwd, title='Choose a file to decrypt...')
            print(filename)
            print('Select the private key to decrypt the file with.')
            Tk().withdraw()
            keypath = askopenfilename(initialdir=cwd, title='Choose a private key...')
            print(keypath)
            print('Select the encrypted key file used to encrypt the file.')
            Tk().withdraw()
            keyfilepath = askopenfilename(initialdir=cwd, title='Choose the encrypted key file...')
            print(keyfilepath)
            print('Select the name for the decrypted file.')
            Tk().withdraw()
            outfile = asksaveasfilename(initialdir=cwd, title='Save as...')
            print(outfile)
            chunksize = input('Select chunksize (leave empty for default): ') or 24 * 1024
            rsa.decrypt(keypath, filename, keyfilepath, outfile, chunksize)

        elif action == '3':
            exit(0)

    elif action == '4':
        title('RSA Signature / verification', fillchar='-')
        [print() for i in range(5)]
        print('Do you want to...')
        print('1. Sign a file')
        print('2. Verify a file')
        print('3. Exit')
        print('_' * utils.get_terminal_size()[0])
        print()
        action = input('>> ').lower()

        if action == '1':
            title('RSA Signature / verification', fillchar='-')
            print(); print()
            print('Select file to sign...')
            Tk().withdraw()
            filename = askopenfilename(initialdir=cwd, title='Select file to sign...')
            print(filename)
            print('Select private key...')
            Tk().withdraw()
            privKey = askopenfilename(initialdir=cwd, title='Select private key...')  
            print(privKey)
            print('Select name for signature file...')
            signature = asksaveasfilename(initialdir=cwd, title='Select signature filename...') or None
            print(signature)
            sign(filename, privKey, signature)
        

        elif action == '2':
            title('RSA Signature / verification', fillchar='-')
            print(); print()
            print('Select file to verify...')
            Tk().withdraw()
            filename = askopenfilename(initialdir=cwd, title='Select file to verify...')
            print(filename)
            print('Select public key...')
            Tk().withdraw()
            pubKey = askopenfilename(initialdir=cwd, title='Select public key...')  
            print(pubKey)
            print('Select signature file...')
            signature = askopenfilename(initialdir=cwd, title='Select signature file...')
            print(signature)
            valid = verify(filename, signature, pubKey)
            if valid:
                print('Success! Signature and hash are the same, so the file has not been tampered with.')
                _tmp = input('Press enter to continue...')
            elif not valid:
                clear()
                print('FILE AUTHENTICITY COULD NOT BE VERIFIED!')
                print('Do not trust the file or its sender. Did you use the correct public key?')
                print('Error: Verification failed. Authenticity of file could not be verified.')
            

        elif action == '3':
            pass

    else:
        TypeError('invalid action: \'%s\' in RSA()')

parser = argparse.ArgumentParser(description="AES and RSA cryptography tools")
parser.add_argument('--debug', help="Wait for debugger to attach on port (default is 3000)",
                               dest='port',
                               default=None,
                               const='5768',
                               nargs='?',
                               type=int)
args = parser.parse_args()

title('Crypto 2.0!')
[print() for i in range(5)]
print('What do you want to do?')
print("1. Encrypt/decrypt a file with AES")
print("2. Generate RSA keys")
print("3. Encrypt/decrypt a file with RSA")
print('4. Sign a file using RSA')
print()
print('Type the number corresponding to the desired action.')
print('Type q, quit or ctrl-c to quit.')
if args.port:
    print('Port is %s' % args.port)
print('_' * utils.get_terminal_size()[0])
print()
try:
    action = input('> ').lower()
except KeyboardInterrupt:
    clear()
    exit(0)

if action == 'q' or action == 'quit':
    clear()
    exit(0)
elif action in ['1', 'aes']:
    AES()
elif action in ['2', '3', '4']:
    RSA(action)
elif action == '4':
    pass
