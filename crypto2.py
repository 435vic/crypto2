import argparse
import tkinter as tk
from time import sleep

import Cryptodome

import utils
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
            

        elif action in ['2', 'decrypt', 'd']:
            pass
        elif action in ['3', 'exit', 'quit', 'q']:
            pass
        else:
            clear()
            _tmp = input('Dude. That is not an action.')


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
