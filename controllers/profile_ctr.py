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
    cookies.reset_all_flags(['modify', 'is_field_mod'])
    if not cookies.contains('modify'):
        cookies.set('modify', False)
    if not cookies.contains('is_field_mod'):
        cookies.set('is_field_mod', {})

def current_roles(user):
    all_roles = ['root', 'admin', 'manager', 'dean', 'default']
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

def set_flags(flags, form):
    flags.set('is_mod_phone', 'button_phone' in form and 'phone' not in form)
    flags.set('is_mod_name' , 'button_name'  in form and 'name'  not in form)
    flags.set('is_mod_addr' , 'button_addr'  in form and 'addr'  not in form)
    flags.set('is_mod_carne', 'button_carne' in form and 'carne' not in form)

def execute_if_modification(user, flags, form):
    if 'phone' in form:
        update_profile_field(user, 'phone', form['phone'])
        flags.set('is_mod_phone', False)
        return True
    if 'name' in form:
        update_profile_field(user, 'name', form['name'])
        flags.set('is_mod_name', False)
        return True
    if 'addr' in form:
        update_profile_field(user, 'address', form['addr'])
        flags.set('is_mod_addr', False)
        return True
    if 'carne' in form:
        update_profile_field(user, 'id', form['carne'])
        flags.set('is_mod_carne', False)
        return True
    if any(flags.get(x) for x in flags.dictionary):
        return True
    return False

def add_quota_bonus(user, bonus, comment, until):
    return db.query('''insert into QuotaBonus (username, bonus, comment, expires)
                    values(\'{0}\',\'{1}\',\'{2}\',\'{3}\')'''.format(user, bonus, comment, until))

def update_profile_field(username, column, value):
    return db.query('''update Users set {0} = \'{1}\'
                    where UserName = \'{2}\''''.format(column, value, username), False)

def update_password(username, password):
    return db.query('''update Users set Password = \'{0}\'
                    where UserName = \'{1}\''''.format(password, username), False)

def update_rol(user, rol):
    return db.query('update DBRoles set roles = \'{0}\' where username = \'{1}\''.format(rol, user), False)

def get_roles(username):
    return db.query('''select roles, username
                        from DBRoles
                        where username= \'{0}\''''.format(username))