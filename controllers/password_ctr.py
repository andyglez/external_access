from settings import email, database as db, encryption as cr
from languages import messages as msg

def check_info(user, e_addr, mail, lang='es'):
    result = db.query('select username, id from Users where username = \'{0}\' and email = \'{1}\''.format(user, e_addr))
    if len(result) == 0:
        return False, msg.user_not_found(user, lang)
    (user, dni) = result[0]
    email.send_new_pass(mail, user, dni, e_addr)
    return True, msg.check_your_email(lang)

def verify_email(user, pwd, conf, lang='es'):
    if pwd != conf:
        return False, msg.mismatch_new_password(lang)
    password = cr.encrypt(pwd)
    db.query('update Users set password = \'{0}\' where username = \'{1}\''.format(password, user), False)
    return True, msg.successfull_pass_change(lang)
