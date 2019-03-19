def wrong_user_pass(language='es'):
    message = {
        'en': 'Wrong username or password',
        'es': 'Usuario o contraseña incorrectos',
        'ca': 'Usuari o contrasenya incorrectes'
    }
    return message[language]

def user_already_exists(username, language='es'):
    message = {
        'en': 'User '+username+' already exists',
        'es': 'El usuario '+username+' ya existe',
        'ca': 'L\'usuari ' +username+' ja existeix'
    }
    return message[language]

def phone_already_in_use(phone, language='es'):
    message = {
        'en': 'Phone '+phone+' is already anchored to another account',
        'es': 'El teléfono '+phone+' ya está anclado a otra cuenta',
        'ca': 'El teléfon '+phone+' ja està ancorat amb altre conta'
    }
    return message[language]

def request_sent_successfully(language='es'):
    message = {
        'en': 'Successfull operation. Contact with your network admin within a few days',
        'es': 'Operación exitosa. Contacte con su administrador de red en un par de días',
        'ca': 'Operació exitosa. Contacti l\'administrador de la xarxa en uns dies'
    }
    return message[language]

def logout_successful(language='es'):
    message = {
        'en' : 'Logout successfull',
        'es' : 'Su sesión ha cerrado exitosamente',
        'ca' : 'La seva sessió ha tancat amb èxit'
    }
    return message[language]

def bad_password(language='es'):
    message = {
        'en' : 'Wrong Password',
        'es' : 'Contraseña incorrecta',
        'ca' : 'Contrasenya incorrecta'
    }
    return message[language]

def mismatch_new_password(language='es'):
    message = {
        'en' : 'New and Verify Password fields must match',
        'es' : 'Los campos Nueva y Verifique Contraseña deben coincidir',
        'ca' : 'Els camps Nova i Verifiqui Contrasenya deuen coincidir'
    }
    return message[language]

def get_headers(language='es'):
    phone = {
        'en': 'Phone',
        'es': 'Teléfono',
        'ca': 'Teléfon'
    }
    start_time = {
        'en': 'Start Time',
        'es': 'Tiempo de Inicio',
        'ca': 'Temps d\'inici'
    }
    stop_time = {
        'en': 'Stop Time',
        'es': 'Tiempo Final',
        'ca': 'Temps de final'
    }
    consumed = {
        'en': 'Consumed',
        'es': 'Consumido',
        'ca': 'Consumit'
    }
    return [phone[language], start_time[language], stop_time[language], consumed[language]]