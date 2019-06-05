from settings import database as db, encryption as cr, email
from languages import messages as msg
from datetime import datetime
from flask import url_for
from suds.client import Client
import urllib
import ssl


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
    result = ('test_name', 'test_dni', 'test_address')#consume_webservice(form['email'])
    if result == -1:
        return 'error'
    (name, dni, address) = result
    insert_into_pending(username, name, crypted, area, dni, form['email'], address, form['phone'], datetime.now().isoformat(), 'default', '')

    #coworkers = db.query('select username, email from Users where area = \'{0}\''.format(area))
    #dean = [y for (x, y) in coworkers if len(db.query('select (username) from DBRoles where roles = \'dean\' and username = \'{0}\''.format(x))) > 0][0]

    #data = (name, form['email'], area, address)
    #send_mail(mail, username, dni, dean, data)
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
    url = 'https://login.uh.cu/WebServices/CuoteService.asmx?WSDL'
    ssl._create_default_https_context = ssl._create_unverified_context
    client = Client(url)

    try:
        results = client.service.DatosTrabajador(mail)
        if not bool(results):
            return -1
        else:
            return results[0][0]
    except:
        return -1

def send_mail(mail, username, dni, dean, data):
    (name, e_addr, area, address) = data
    mail_objectives = email.get_mail_authorizers()
    mail_objectives.append(dean)
    for x in mail_objectives:
        email.send_auth_request(mail,
        'El usuario ' + username + ' ha sido correctamente validado en los servicios directorios de la Universidad\n' +
        'Su información personal completa es la siguiente:\n' +
        'Nombre : ' + name + '\n' +
        'E-mail : ' + e_addr + '\n' + 
        'Area   : ' + area + '\n' + 
        'Direc. : ' + address + '\n' +
        'Para completar la autorización del usuario dé click en el siguiente enlace\n' +
        'http://accesotelefonico.uh.cu'+url_for('authorize', username=username, dni=dni, author=x.split('@')[0]), recip=x)
