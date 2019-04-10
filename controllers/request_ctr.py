from settings import database as db, encryption as cr
from languages import messages as msg

def is_a_valid_request(username, phone, lang):
    data = check_existance(username)
    if len(data) > 0:
        return (False, msg.user_already_exists(username, lang))
    data = check_phone(phone)
    if len(data) > 0:
        return (False, msg.phone_already_in_use(lang))
    return (True, '')

def make_request(form, lang):
    full_name = form['name'] + ' ' + form['last_name']
    crypted = cr.encrypt(form['password'])
    insert_into_pending(form['user'], full_name, crypted, form['phone'])
    return msg.request_sent_successfully(lang)

def check_existance(username):
    return db.query('select * from Users where Username=\'{}\''.format(username))

def check_phone(phone):
    return db.query('select * from Pending where phone=\'{}\''.format(phone))

def insert_into_pending(username, fullname, password, phone):
    return db.query('''insert into Pending (username, name, password, phone)
                        values(\'{0}\',\'{1}\',\'{2}\',\'{3}\')'''.format(username, fullname, password, phone), False)