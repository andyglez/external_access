from settings import database as db, encryption as cr, email
from languages import messages as msg
from datetime import datetime
from flask import url_for
from utils import userinfo

def is_a_valid_request(form, lang):
    if form['user'] == '':
        return (False, msg.request_authorization_messages('user', 'empty', lang))
    if form['email'] == '':
        return (False, msg.request_authorization_messages('email', 'empty', lang))
    if form['phone'] == '':
        return (False, msg.request_authorization_messages('phone', 'empty', lang))
    data = check_email(form['email'])
    if len(data) > 0:
        return (False, msg.email_already_in_use(lang))
    data = check_existance(form['user'])
    if len(data) > 0:
        return (False, msg.user_already_exists(lang))    
    if form['password'] != form['confirm']:
        return (False, msg.mismatch_new_password(lang))
    if len(form['phone']) != 8:
        return (False, msg.request_authorization_messages('phone', 'length', lang))
    aux = form['email'].split('@')
    if len(aux) != 2:
        return (False, msg.request_authorization_messages('email', 'miss', lang))
    if len(aux[1].split('.')) != 3:
        return (False, msg.request_authorization_messages('email', 'addr', lang))
    if form['name'] == '':
        return (False, msg.request_authorization_messages('name', 'empty', lang))
    if form['dni'] == '':
        return (False, msg.request_authorization_messages('dni', 'empty', lang))
    if form['address'] == '':
        return (False, msg.request_authorization_messages('address', 'empty', lang))
    return (True, '')

def make_request(username, mail, form, lang):
    crypted = cr.encrypt(form['password'])
    area = process_info(form['email'])
    result = userinfo.consume_webservice(form['email'])
    if result == -1:
        return 'error'
    (name, dni, address) = (form['fullname'], form['dni'], form['address'])
    insert_into_pending(username, name, crypted, area, dni, form['email'], address, form['phone'], datetime.now().isoformat(), 'default', '')

    coworkers = db.query('select username, email from Users where area = \'{0}\''.format(area))
    dean = [y for (x, y) in coworkers if len(db.query('select (username) from DBRoles where roles = \'dean\' and username = \'{0}\''.format(x))) > 0][0]

    data = (name, form['email'], area, address)
    email.send_mail_to_dean(mail, username, dni, dean, data)
    email.notify_user(mail, username, form['email'], 'start')
    return msg.request_sent_successfully(lang)

def check_existance(username):
    return db.query('select * from Users where Username=\'{}\''.format(username))

def check_email(mail):
    return db.query('select * from Pending where email=\'{}\''.format(mail))

def insert_into_pending(username, name, password, area, dni, email, address, phone, notes, group, auth):
    return db.query('''insert into Pending (username, name, password, area, id, email, address, phone, notes, groupname, authorized_by)
                        values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\',\'{9}\',\'{10}\')'''
                        .format(username, name, password, area, dni, email, address, phone, notes, group, auth), False)

def process_info(mail):
    aux = mail.split('@')
    area = aux[1].split('.')[0]
    return area


