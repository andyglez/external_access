from settings import database as db

def check_pending(username, dni, author):
    data = db.query('select * from Pending where username = \'{}\''.format(username))
    if len(data) == 0:
        return False
    if len(data[0][-1].split(',')) > 2:
        return False

    coworkers = db.query('select username, email from Users where area = \'{0}\''.format(data[0][3]))
    dean = [y for (x, y) in coworkers if len(db.query('select (username) from DBRoles where roles = \'dean\' and username = \'{}\''.format(x))) > 0][0]
    if author != dean:
        return False
    return True

def update_auth(username, dni, author):
    data = db.query('select * from Pending where username = \'{}\''.format(username))
    if data[0][-1] == '':
        db.query('update Pending set authorized_by = \'{0}\' where username = \'{1}\''.format(author, username))
    elif len(data[0][-1].split(',') <= 2) and author not in data[0][-1]:
        db.query('update Pending set authorized_by = \'{0}\' where username = \'{1}\''.format(data[0][-1] + ',' + author, username))
    elif author not in data[0][-1]:
        user, name, pwd, area, idn, email, address, phone, notes, group, _ = data[0]
        db.query('''insert into Users (UserName, Name, Password, Area, id, email, address, phone, notes, GroupName)
                values (\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\', \'{6}\', \'{7}\', \'{8}\', \'{9}\')'''
                .format(user, name, pwd, area, idn, email, address, phone, notes, group), False)
        db.query('delete from Pending where username = \'{}\''.format(username))
    return 0