import argparse
import os
from getpass import getpass
from time import sleep
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilename, asksaveasfilename

import Cryptodome

import utils
import aes
import rsa
from utils import clear, title


def AES():
    while True:
        title('AES Encryption / Decryption', fillchar='-')
        [print() for i in range(8)]
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
            filename = askopenfilename(initialdir='~', title='Choose a file to encrypt...')
            password = getpass('Enter password for file: ').encode('utf-8')
            print('Choose the name for the encrypted file.')
            outfilename = asksaveasfilename(initialdir='~', title='Choose the name for the encrypted file...')
            chunksize = input('Enter encryption chunksize: ') or None
            if chunksize:
                chunksize = int(chunksize)
            aes.encrypt(password, filename, outfilename, chunksize)

        elif action in ['2', 'decrypt', 'd']:
            title('AES Encryption / Decryption', fillchar='-')
            print(); print()
            print('Please select a file in the dialog box.')
            Tk().withdraw()
            filename = askopenfilename(initialdir='~', title='Choose a file to decrypt...')
            password = getpass('Enter password to decrpyt file: ').encode('utf-8')
            print('Choose the name for the output file.')
            outfilename = asksaveasfilename(initialdir='~', title='Choose the name for the decrypted file...')
            chunksize = input('Enter decryption chunksize: ') or None
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
            outfolder = askdirectory(initialdir='~', title='Select directory to save keys in...')
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
        [print() for i in range(8)]
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
            filename = askopenfilename(initialdir='~', title='Choose a file to encrypt...')
            print('Select the public key to encrypt the file with.')
            Tk().withdraw()
            keypath = askopenfilename(initialdir='~', title='Choose a public key...')
            print('Select the name for the encrypted file.')
            Tk().widthdraw()
            outfile = asksaveasfilename(initialdir='~', title='Save as...')
            chunksize = input('Select chunksize (leave empty for default): ') or None
            rsa.encrypt(keypath, filename, outfile, chunksize)
        
        elif action == '2':
            title('RSA Encryption / Decryption', fillchar='-')
            print(); print()
            print('Select a file to decrypt in the dialog box.')
            Tk().withdraw()
            filename = askopenfilename(initialdir='~', title='Choose a file to decrypt...')
            print('Select the private key to decrypt the file with.')
            Tk().withdraw()
            keypath = askopenfilename(initialdir='~', title='Choose a private key...')
            print('Select the encrypted key file used to encrypt the file.')
            Tk().withdraw()
            keyfilepath = askopenfilename(initialdir='~', title='Choose the encrypted key file...')
            print('Select the name for the decrypted file.')
            Tk().widthdraw()
            outfile = asksaveasfilename(initialdir='~', title='Save as...')
            chunksize = input('Select chunksize (leave empty for default): ') or None
            rsa.decrypt(keypath, filename, keyfilepath, outfile, chunksize)


    elif action == '4':
        pass
    else:
        TypeError('invalid action: \'%s\' in RSA()')

#TODO: Look at default port in python: attach command 
parser = argparse.ArgumentParser(description="AES and RSA cryptography tools")
parser.add_argument('--debug', help="Wait for debugger to attach on port (default is 3000)",
                               dest='port',
                               default=None,
                               const='3000',
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
