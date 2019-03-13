def check_root(roles):
    return True if 'root' in roles else False

def check_admin(roles):
    return True if 'admin' in roles else False
        
def check_dean(roles):
    return True if 'dean' in roles else False

def check_ddi(roles):
    return True if 'ddi' in roles else False

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

def get_user_quota(group):
    session, _ = group[0]
    roaming, _ = group[1]
    return {
        'value': session,
        'roaming': roaming
    }