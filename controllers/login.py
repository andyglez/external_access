from utils.cookies import Cookies
from settings import database as db, encryption as cr
from utils import userinfo
from languages import messages as msg

def set_cookies(cookies):
    cookies.set('current', 'start')
    if not cookies.contains('lang'):
        cookies.set('lang', 'es')

def check_user_login(user, password, cookies):
    data = get_basic_info(user)
    if len(data) == 0 or not cr.check(password, data[0][1]):
        return (False, msg.wrong_user_pass(cookies.get('lang')))
    result, _ = get_roles(user)
    cookies.set('user', user)
    cookies.set('group', data[0][-1])
    cookies.set('roles', userinfo.get_user_roles(result.split(',')))
    v = get_profile_data(user)
    cookies.set('info', v[0] if len(v) > 0 else v)
    cookies.set('area', v[0][2])
    cookies.set('phone', v[0][5])
    cookies.set('headers', msg.get_headers(cookies.get('lang')))
    return (True, '')

def get_basic_info(username):
    return db.query('''select UserName, Password, GroupName
                        from Users 
                        where UserName= \'{0}\''''.format(username))

def get_roles(username):
    return db.query('''select roles, username
                from DBRoles
                where username= \'{0}\''''.format(username))[0]

def get_profile_data(username):
    return db.query('''select UserName, Name, Area, email, address, phone, id, Password
                        from Users
                        where Username = \'{}\''''.format(username))