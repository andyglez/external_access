from settings import database as db, encryption as cr
from utils.cookies import Cookies
from datetime import datetime
from languages import messages as msg

def dont_have_permissions(roles):
    return not(roles['is_root'])

def load_visual_options():
    groups = [x[0] for x in get_group_names()]
    roles = ['root', 'admin', 'manager', 'dean', 'default']
    areas = [x[0] for x in get_areas()]
    return (groups, roles, areas)

def duplicate_error(user, lang):
    return msg.user_already_exists(user, lang)

def create_user(form, lang):
    crypted = cr.encrypt(form['pass'])
    data = (form['user'], form['name'], crypted, form['area'],
    form['id'], form['email'], form['address'], form['phone'],
    form['notes'], form['group'], form['authorized'] if form['authorized'] else datetime.today().isoformat())
    insert_new_user(data)
    insert_into_dbroles(form['user'], form['roles'])
    return msg.user_creation_successfull(lang)

def get_group_names():
    return db.query('select GroupName from radgroupcheck where id < 5')

def get_areas():
    return db.query('select Area from Areas')

def insert_new_user(data):
    user, name, pwd, area, idn, email, address, phone, notes, group, auth = data
    return db.query('''insert into Users (UserName, Name, Password, Area, id, email, address, phone, notes, GroupName, autorizo_hasta)
                    values (\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\', \'{6}\', \'{7}\', \'{8}\', \'{9}\', \'{10}\')'''
                    .format(user, name, pwd, area, idn, email, address, phone, notes, group, auth), False)

def insert_into_dbroles(user, rol):
    return db.query('insert into DBRoles (username, roles) values (\'{0}\', \'{1}\')'.format(user, rol), False)