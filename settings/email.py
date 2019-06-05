from flask_mail import Mail, Message
from flask import url_for

mail_server = 'smtp.uh.cu'
#mail_port = 465
mail_username = 'accesotelefonico@uh.cu'
#mail_password = '***'
#mail_use_tls = False
#mail_use_ssl = True

def get_mail_authorizers():
    return []

def send_auth_request(mail, body, recip):
    msg = Message(subject='Petición de Autorización', recipients=[recip], sender=mail_username)
    msg.body = body
    mail.send(msg)

def send_new_pass(mail, user, dni, recip):
    msg = Message(subject='Nueva Contraseña', recipients=[recip], sender=mail_username)
    msg.body = 'Hola {0}. Pulse en el siguiente enlace para modificar su contraseña:\n'.format(user)
    msg.boyd = msg.body + 'http://accesotelefonico.uh.cu' + url_for('confirm_password', user=user, dni=dni, e_addr=recip)
    mail.send(msg)

def set_mail(config):
    config['MAIL_SERVER']= mail_server
    #config['MAIL_PORT'] = mail_port
    config['MAIL_USERNAME'] = mail_username
    #config['MAIL_PASSWORD'] = mail_password
    #config['MAIL_USE_TLS'] = mail_use_tls
    #config['MAIL_USE_SSL'] = mail_use_ssl
