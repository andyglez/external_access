from suds.client import Client
import urllib
import ssl

def check_root(roles):
    return True if 'root' in roles else False

def check_admin(roles):
    return True if 'admin' in roles else False
        
def check_dean(roles):
    return True if 'dean' in roles else False

def check_ddi(roles):
    return True if 'manager' in roles else False

def check_default(roles):
    return True if 'default' in roles else False


def get_user_roles(roles):
    return {
        'is_root': check_root(roles),
        'is_admin': check_admin(roles),
        'is_dean': check_dean(roles),
        'is_ddi': check_ddi(roles),
        'is_default': check_default(roles)
    }

def get_user_quota(group, bonus):
    session, _ = group[len(group) - 2]
    roaming, _ = group[len(group) - 1]
    b = sum([x for x,_ in bonus])
    return {
        'total': int(session) + b,
        'value': int(session),
        'roaming': int(roaming),
        'bonus': b
    }

def percentage(consumed, total):
    return consumed * 100 / total

def consume_webservice(mail):
    url = 'https://login.uh.cu/WebServices/CuoteService.asmx?WSDL'
    ssl._create_default_https_context = ssl._create_unverified_context

    try:
        client = Client(url)
        results = client.service.DatosTrabajador(mail)
        if not bool(results):
            return -1
        else:
            return results[0][0]
    except:
        return -1
