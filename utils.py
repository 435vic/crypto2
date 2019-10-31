import platform
import os

def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def title(text, width=None, fillchar='='):
    if width == None:
        if get_terminal_size():
            width = get_terminal_size()[0]
    clear()
    print(fillchar * width)
    print()
    print(('%s' % text).center(width, ' '))
    print()
    print(fillchar * width)

    
def get_terminal_size():
    try:
        size = os.get_terminal_size()
        return size
    except OSError:
        return None
