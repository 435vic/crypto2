import argparse
from getpass import getpass
from time import sleep
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

import Cryptodome

import utils
from aes import decrypt, encrypt
from utils import clear, title
from window import Window


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
            encrypt(password, filename, outfilename, chunksize)

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
            decrypt(password, filename, outfilename, chunksize)

        elif action in ['3', 'exit', 'quit', 'q']:
            exit(0)

        else:
            clear()
            _tmp = input('Dude. That is not an action.')

def RSA(action):
    if action == 'g':
        pass

    elif action == 'ed':
        pass
    elif action == 's':
        pass
    else:
        print('Invalid action: \'%s\' in RSA()' % action)

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
elif action == '1':
    AES()
