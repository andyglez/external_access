from settings import database as db, encryption as cr
from languages import messages as msg

def is_a_valid_request(username, email, lang):
    data = check_existance(username)
    if len(data) > 0:
        return (False, msg.user_already_exists(username, lang))
    data = check_email(email)
    if len(data) > 0:
        return (False, msg.email_already_in_use(lang))
    return (True, '')

def make_request(form, lang):
    full_name = form['name'] + ' ' + form['last_name']
    crypted = cr.encrypt(form['password'])
    insert_into_pending(form['user'], form['email'], full_name, crypted, form['phone'])
    return msg.request_sent_successfully(lang)

def check_existance(username):
    return db.query('select * from Users where Username=\'{}\''.format(username))

def check_email(email):
    return db.query('select * from Pending where email=\'{}\''.format(email))

def insert_into_pending(username, email, fullname, password, phone):
    return db.query('''insert into Pending (username, email, name, password, phone)
                        values(\'{0}\',\'{1}\',\'{2}\',\'{3}\')'''.format(username, email, fullname, password, phone), False)