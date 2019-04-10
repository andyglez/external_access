from settings import database as db
from utils.cookies import Cookies

def dont_have_permissions(roles):
    return roles['is_default']

def search(cookies, query):
    data = ([(u, n, a) for u, n, a in get_users() if query in n.lower() and a == cookies.get('info')[2]] 
            if cookies.get('roles')['is_dean'] or cookies.get('roles')['is_admin']
            else [(u, n, a) for u, n, a in get_users() if query in n.lower()])
    cookies.set('query_value', query)
    return data

def get_users():
    return db.query('select UserName, Name, Area from Users')