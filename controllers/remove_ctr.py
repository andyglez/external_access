from settings import database as db
from utils.cookies import Cookies

def dont_have_permissions(roles):
    return not(roles['is_dean'] or roles['is_root'])

def log_removal(user, name, area, executor, reason):
    insert_removed_user(user, name, area, executor, reason)
    delete_users(user)

def insert_removed_user(username, name, area, executor, reason):
    return db.query('''insert into RemovedUsers (username, name, area, removed_by, reason)
                    values(\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\')'''.format(username, name, area, executor, reason), False)

def delete_users(username):
    return db.query('delete from Users where UserName = \'{0}\''.format(username))