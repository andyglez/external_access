from subprocess import Popen, PIPE
#Configuration file for setting different modes of encryption to use with the freeradius database
#Modes can be 'plain' or 'radcrypt simple'
mode = 'radcrypt simple'

def encrypt(text):
    if mode == 'plain':
        return text
    elif 'radcrypt' in mode:
        if 'simple' in mode:
            p = Popen(["radcrypt", text], stdout=PIPE, stderr=PIPE, universal_newlines=True)
            output, _ = p.communicate()
            return "".join([x for x in output if x != '\n'])
        else:
            return ''
    return ''

def check(text, crypted):
    if mode == 'plain':
        return text == crypted
    elif 'radcrypt' in mode:
        if 'simple' in mode:
            p = Popen(["radcrypt", "-c", text, crypted], stdout=PIPE, stderr=PIPE, universal_newlines=True)
            output, _ = p.communicate()
            return 'OK' in output
        else:
            return False
    return False