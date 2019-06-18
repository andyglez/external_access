def wrong_user_pass(language='es'):
    message = {
        'en': 'Wrong username or password',
        'es': 'Usuario o contraseña incorrectos',
        'ca': 'Usuari o contrasenya incorrectes'
    }
    return message[language]

def user_not_found(email, language='es'):
    message = {
        'en': 'Email '+email+' is not associated to any account',
        'es': 'El correo '+email+' no está asociado a ninguna cuenta',
        'ca': 'El correu '+email+' no és associat a cap compte'
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

def bad_webservice_return(email, language='es'):
    message = {
        'en': 'Email ' +email+ ' is incorrect',
        'es': 'El correo ' + email + ' es incorrecto',
        'ca': 'El correu ' + email + ' es incorrecte'
    }
    return message[language]

def dni_too_long(language='es'):
    message = {
        'en' : 'DNI must be at most of 11 characters',
        'es' : 'El carnet debe ser de 11 caracteres a lo sumo',
        'ca' : 'El DNI ha de ser quan més de 11 nombres'
    }
    return message['language']

def no_dean_error(language='es'):
    message = {
        'en' : 'Error. Please contact with your administrator',
        'es' : 'Error. Por favor contacte con su administrador',
        'ca' : 'Error. Contacti amb el seu administrador si us plau'
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
        },
        'name' : {
            'empty' :{
                'en' : 'Name field can\'t be empty',
                'es' : 'El campo Nombre no debe estar vacío',
                'ca' : 'El camp Nom no ha de ser vacu'
            }
        },
        'dni' : {
            'empty' :{
                'en' : 'DNI field can\'t be empty',
                'es' : 'El campo Carnet de Identidad no debe estar vacío',
                'ca' : 'El camp DNI no ha de ser vacu'
            }
        },
        'address' : {
            'empty' :{
                'en' : 'Address field can\'t be empty',
                'es' : 'El campo Dirección no debe estar vacío',
                'ca' : 'El camp Adreça no ha de ser vacu'
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
