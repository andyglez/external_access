from subprocess import Popen, PIPE
#Configuration file for setting different modes of encryption to use with the freeradius database
#Modes can be 'plain' or 'radcrypt simple'
mode = 'plain'

def encrypt(text):
    if mode == 'plain':
        return text
    elif 'radcrypt' in mode:
        if 'simple' in mode:
            p = Popen(["radcrypt", text], stdout=PIPE, stderr=PIPE, universal_newlines=True)
            output, _ = p.communicate()
            return output
        else:
            return ''
    return ''
