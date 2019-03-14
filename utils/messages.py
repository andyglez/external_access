def wrong_user_pass(language='es'):
    message = {
        'en': 'Wrong username or password',
        'es': 'Nombre de usuario o contraseña incorrectos'
    }
    return message[language]

def user_already_exists(username, language='es'):
    message = {
        'en': 'User '+username+' already exists',
        'es': 'El usuario \''+username+'\' ya existe'
    }
    return message[language]

def phone_already_in_use(phone, language='es'):
    message = {
        'en': 'Phone '+phone+' is already anchored to another account',
        'es': 'El teléfono '+phone+' ya está anclado a otra cuenta'
    }
    return message[language]

def request_sent_successfully(language='es'):
    message = {
        'en': 'Successfull operation. Contact with your network admin within a few days',
        'es': 'Operación exitosa. Contacte con su administrador de red en un par de días'
    }
    return message[language]