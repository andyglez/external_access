from flask_mail import Mail, Message
from flask import url_for

mail_server = 'smtp.uh.cu'
#mail_port = 465
mail_username = 'accesotelefonico@uh.cu'
#mail_password = '***'
#mail_use_tls = False
#mail_use_ssl = True

def send_auth_request(mail, body, recip):
    msg = Message(subject='Petición de Autorización', recipients=[recip], sender=mail_username)
    msg.body = body
    mail.send(msg)

def send_new_pass(mail, user, dni, recip):
    msg = Message(subject='Nueva Contraseña', recipients=[recip], sender=mail_username)
    msg.body = 'Hola {0}. Pulse en el siguiente enlace para modificar su contraseña:\n'.format(user)
    msg.body = msg.body + 'http://accesoremoto.uh.cu' + url_for('confirm_password', user=user, dni=dni, e_addr=recip)
    mail.send(msg)

def notify_user(mail, user, recip, action):
    if action == 'start':
        msg = Message(subject='Bienvenido a Acceso Remoto', recipients=[recip], sender=mail_username)
        msg.body = 'Hola {0}.\nUsted ha enviado su petición de autorización al servicio de Acceso Remoto\n'.format(user)
        msg.body = msg.body + 'Verifique regularmente su buzón para que esté al tanto del proceso que lo autoriza.'
        mail.send(msg)
    elif action == 'dean':
        msg = Message(subject='Autorización del Servicio', recipients=[recip], sender=mail_username)
        msg.body = 'Hola {0}.\nSu petición ha sido procesada con éxito.\nVisite a su decano o jefe de área para obtener sus datos.'
        mail.send(msg)
    elif action == 'ddi':
        msg = Message(subject='Usuario Confirmado', recipients=[recip], sender=mail_username)
        msg.body = 'Hola {0}.\nSu autorización ha sido confirmada y su usuario ha sido habilitado.\n'
        msg.body = msg.body + 'Visite el sitio de información que se encuentra en http://accesoremoto.uh.cu'
        mail.send(msg)

def send_mail_to_dean(mail, username, dni, dean, data):
    (name, e_addr, area, address) = data
    mail_objectives = []
    mail_objectives.append(dean)
    for x in mail_objectives:
        send_auth_request(mail,
        '''El usuario {0} ha sido correctamente validado en los servicios directorios de la Universidad
Su información personal completa es la siguiente:
Nombre : {1}
E-mail : {2}
Area   : {3}
Direc. : {4}
Para completar la autorización visite la aplicación el siguiente enlace http://accesoremoto.uh.cu'''.format(username, name, e_addr, area, address), recip=x)

def set_mail(config):
    config['MAIL_SERVER']= mail_server
    #config['MAIL_PORT'] = mail_port
    config['MAIL_USERNAME'] = mail_username
    #config['MAIL_PASSWORD'] = mail_password
    #config['MAIL_USE_TLS'] = mail_use_tls
    #config['MAIL_USE_SSL'] = mail_use_ssl
