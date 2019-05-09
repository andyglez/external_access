from settings import database as db, encryption as cr, email
from languages import messages as msg
from datetime import datetime
from flask import url_for

def is_a_valid_request(mail_address, lang):
    data = check_email(mail_address)
    if len(data) > 0:
        return (False, msg.email_already_in_use(lang))
    aux = mail_address.split('@')
    if len(aux) > 2:
        return (False, 'error')
    if len(aux[1].split('.')) != 3:
        return (False, 'error')
    return (True, '')

def make_request(mail, form, lang):
    crypted = cr.encrypt(form['password'])
    (username, area) = process_info(form['email'])
    (name, dni, address) = consume_webservice(form['email'])
    insert_into_pending(username, name, crypted, area, dni, form['email'], address, form['phone'], datetime.now().isoformat(), 'default', '')

    coworkers = db.query('select username, email from Users where area = \'{0}\''.format(area))
    dean = [y for (x, y) in coworkers if len(db.query('select (username) from DBRoles where roles = \'dean\' and username = \'{}\''.format(x))) > 0][0]
    #print(dean)
    send_mail(mail, username, dni)
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
    username = aux[0]
    area = aux[1].split('.')[0]
    return (username, area)

def consume_webservice(mail):
    return 'Prueba','99999999999','Dummylandia'

def send_mail(mail, username, dni):
    email.send_auth_request(mail, 'http://tesis.home.cu'+url_for('authorize', username=username, dni=dni, author='andy'))