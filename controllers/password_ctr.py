from settings import email, database as db

def check_info(user, e_addr, mail):
    result = db.query('select username, id from Users where username = \'{0}\' and email = \'{1}\''.format(user, e_addr))
    if len(result) == 0:
        return False, 'Usuario no encontrado'
    email.send_new_pass(mail, user, result[1], e_addr)
    return True, 'Verifique su correo'

def verify_email(user, pwd, conf):
    if pwd != conf:
        return False, 'Los campos no coinciden'
    db.query('update Users set password = \'{0}\' where username = \'{1}\''.format(pwd, user), False)
    return True, 'Contraseña cambiada con exito'
