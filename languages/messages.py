def wrong_user_pass(language='es'):
    message = {
        'en': 'Wrong username or password',
        'es': 'Usuario o contraseña incorrectos',
        'ca': 'Usuari o contrasenya incorrectes'
    }
    return message[language]

def user_not_found(username, language='es'):
    message = {
        'en': 'User '+username+' doesn\'t exist',
        'es': 'Usuario '+username+' no existe',
        'ca': 'Usuari '+username+' no existeix'
    }
    return message[language]

def user_already_exists(username, language='es'):
    message = {
        'en': 'User '+username+' already exists',
        'es': 'El usuario '+username+' ya existe',
        'ca': 'L\'usuari ' +username+' ja existeix'
    }
    return message[language]

def email_already_in_use(email, language='es'):
    message = {
        'en': 'Email: '+email+' is already anchored to another account',
        'es': 'La dirección: '+email+' ya está anclado a otra cuenta',
        'ca': 'La direcció: '+email+' ja està ancorat amb altre conta'
    }
    return message[language]

def check_your_email(language='es'):
    message = {
        'en': 'Check your email',
        'es': 'Compruebe el buzón de entrada de su correo',
        'ca': 'Verifiqui la safata d\'entrada del seu correu'
    }
    return message[language]

def request_sent_successfully(language='es'):
    message = {
        'en': 'Successfull operation',
        'es': 'Operación exitosa',
        'ca': 'Operació exitosa'
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

def successfull_pass_change(language='es'):
    message = {
        'en' : 'Password successfully changed',
        'es' : 'Contraseña cambiada con éxito',
        'ca' : 'Contrasenya cambiat amb éxit'
    }
    return message[language]

def user_creation_successfull(language='es'):
    message = {
        'en' : 'User has been created successfully',
        'es' : 'Usuario ha sido creado con éxito',
        'ca' : 'Usuari ha sigut creat amb éxit'
    }
    return message[language]

def request_authorization_messages(field, reason, language='es'):
    options = {
        'user' : {
            'empty' : {
                'en' : 'User field can\'t be empty',
                'es' : 'El campo Usuario no debe estar vacío',
                'ca' : 'El camp Usuari no ha de ser vacu'
            }
        },
        'email' : {
            'empty' : {
                'en' : 'Email field can\'t be empty',
                'es' : 'El campo Correo no debe estar vacío',
                'ca' : 'El camp Correu no ha de ser vacu'
            },
            'miss' : {
                'en' : 'Email must have an @ symbol',
                'es' : 'El correo debe tener el símbolo @',
                'ca' : 'El correu ha de tenir el símbol'
            },
            'addr' : {
                'en' : 'Email must be a subdomain for uh.cu',
                'es' : 'El correo debe ser un sub-dominio de uh.cu',
                'ca' : 'El correu ha de ser un sub-domini de uh.cu'
            }
        },
        'phone' : {
            'empty' : {
                'en' : 'Phone field can\'t be empty',
                'es' : 'El campo Teléfono no debe estar vacío',
                'ca' : 'El camp Teléfon no ha de ser vacu'
            },
            'length' : {
                'en' : 'Phone field must contain 8 digits',
                'es' : 'El campo Teléfono debe contener 8 dígitos',
                'ca' : 'El camp Teléfon ha de contenir 8 dígits'
            }
        }
    }
    return options[field][reason][language]

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