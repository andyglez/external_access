from flask_mail import Mail, Message

mail_server = 'smtp.gmail.com'
mail_port = 465
mail_username = 'id@gmail.com'
mail_password = '***'
mail_use_tls = False
mail_use_ssl = True

def get_mail_authorizers():
    return ['gcobreiro@rect.uh.cu','alina.ruiz@iris.uh.cu']

def send_auth_request(mail, body, recip):
    msg = Message(subject='Auth request', recipients=recip, sender=mail_username)
    msg.body = body
    mail.send(msg)

def set_mail(config):
    config['MAIL_SERVER']= mail_server
    config['MAIL_PORT'] = mail_port
    config['MAIL_USERNAME'] = mail_username
    config['MAIL_PASSWORD'] = mail_password
    config['MAIL_USE_TLS'] = mail_use_tls
    config['MAIL_USE_SSL'] = mail_use_ssl
