from settings import database as db, email as em

def check_pending(username, dni, author):
    data = db.query('select * from Pending where username = \'{}\''.format(username))
    if len(data) == 0:
        return False
    return True

def update_auth(username, dni, author, mail):
    data = db.query('select * from Pending where username = \'{}\''.format(username))
    user, name, pwd, area, idn, email, address, phone, notes, group, _ = data[0]
    db.query('''insert into Users (UserName, Name, Password, Area, id, email, address, phone, notes, GroupName)
                values (\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\', \'{6}\', \'{7}\', \'{8}\', \'{9}\')'''
                .format(user, name, pwd, area, idn, email, address, phone, notes, group), False)
    em.notify_user(mail, username, email, 'ddi')
    db.query('insert into DBRoles (username, roles) values (\'{0}\', \'{1}\')'.format(username, 'default'))
    db.query('delete from Pending where username = \'{}\''.format(username))
    return 0

def authorize_dean_action(name, authorizer, mail):
    e_addr = db.query('select email, id from Pending where username = \'{0}\''.format(name))[0][0]
    em.notify_user(mail, name, e_addr, 'dean')
    db.query('update Pending set authorized_by = \'{0}\' where username = \'{1}\''.format(authorizer, name))
    return 0

def dismiss_action(username, mail):
    e_addr = db.query('select email, id from Pending where username = \'{0}\''.format(username))[0][0]
    em.notify_user(mail, username, e_addr, 'del')
    db.query('delete from Pending where username = \'{0}\''.format(username))
    return 0