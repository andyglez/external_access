from settings import database as db
from utils.cookies import Cookies

def dont_have_permissions(roles):
    return not(roles['is_root'] or roles['is_dean'] or roles['is_ddi'])

def get_data():
    data = get_pendings()
    headers = [x[0] for x in db.query('show columns in Pending') if x[0] != 'password' and x[0] != 'authorized_by']
    return (data, headers)

def get_pendings():
    return db.query('select * from Pending')