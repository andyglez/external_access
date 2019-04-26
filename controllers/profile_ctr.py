from utils.cookies import Cookies
from languages import messages as msg
from settings import encryption as cr, database as db

def check_role_permissions(user, info, cookies):
    if user != cookies.get('user') and cookies.get('roles')['is_default']:
        return True
    if len(info) == 0:
        return True
    if user != cookies.get('user') and cookies.get('roles')['is_dean'] and cookies.get('info')[2] != info[2]:
        return True
    return False

def checked(form, pwd, lang):
    if not cr.check(form['old_password'], pwd):
        return (False, msg.bad_password(lang))
    elif form['new_password'] != form['verify_password']:
        return (False, msg.mismatch_new_password(lang))
    elif form['new_password'] == '':
        return (False, msg.bad_password(lang))
    return (True, msg.successfull_pass_change(lang))

def set_cookies(cookies):
    cookies.reset_all_flags('modify')
    if not cookies.contains('modify'):
        cookies.set('modify', False)

def current_roles(user):
    all_roles = ['root', 'admin', 'ddi', 'dean', 'default']
    rol, _ = get_roles(user)[0]
    roles = [x for x in all_roles if x != rol]
    return (rol, roles)

def save_profile_action(user, form, password, cookies):
    cookies.set('modify', not cookies.get('modify'))
    if 'old_password' in form:
        (flag, msg) = checked(form, password, cookies.get('lang'))
        if flag:
            crypted = cr.encrypt(form['new_password'])
            update_password(user, crypted)
        return (flag, msg)
    elif 'rol' in form:
        update_rol(user, form['rol'])
        cookies.set('modify', False)
        return (True, 'Rol updated')
    return (False, '')

def update_password(username, password):
    return db.query('''update Users set Password = \'{0}\'
                    where UserName = \'{1}\''''.format(password, username), False)

def update_rol(user, rol):
    return db.query('update DBRoles set roles = \'{0}\' where username = \'{1}\''.format(rol, user), False)

def get_roles(username):
    return db.query('''select roles, username
                        from DBRoles
                        where username= \'{0}\''''.format(username))