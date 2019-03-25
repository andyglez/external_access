from datetime import datetime

def get_user(username):
    return '''select UserName, Password, GroupName
                from Users 
                where Username= \'{0}\''''.format(username)

def get_roles(username):
    return '''select roles, username
                from DBRoles
                where username= \'{0}\''''.format(username)

def get_quota(groupname):
    return '''select Value, GroupName
            from radgroupcheck
            where GroupName = \'{}\''''.format(groupname)

def get_quota_bonus(username):
    return '''select Bonus,UserName
            from QuotaBonus
            where UserName = \'{0}\'
            and date_format(Expires, "%Y-%m-%d") > \'{1}\''''.format(username, datetime.now().date().isoformat())

def check_existance(username):
    return 'select * from Users where Username=\'{}\''.format(username)

def check_phone(phone):
    return 'select * from Pending where phone=\'{}\''.format(phone)

def insert_into_pending(username, fullname, password, phone):
    return '''insert into Pending (username, name, password, phone)
            values(\'{0}\',\'{1}\',\'{2}\',\'{3}\')'''.format(username, fullname, password, phone)

def get_acct_consumed(username):
    return '''select UserName,AcctStartTime,AcctStopTime,CallingStationId
                from radacct
                where UserName = \'{0}\'
                and date_format(AcctStartTime, "%Y-%m-%d") >= \'{1}\'
                and date_format(AcctStopTime, "%Y-%m-%d") < \'{2}\''''.format(username
                ,datetime(datetime.now().year, datetime.now().month, 1).date().isoformat()
                ,datetime(datetime.now().year, datetime.now().month, datetime.now().day + 1).date().isoformat())

def get_profile_data(username):
    return '''select UserName, Name, Area, email, address, phone, id, Password
                from Users
                where Username = \'{}\''''.format(username)

def update_password(username, password):
    return '''update Users set Password = \'{0}\'
                where UserName = \'{1}\''''.format(password, username)

def get_users():
    return 'select UserName, Name, Area from Users'

def insert_removed_user(username, name, area, executor, reason):
    return '''insert into RemovedUsers (username, name, area, removed_by, reason)
            values(\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\')'''.format(username, name, area, executor, reason)

def delete_users(username):
    return 'delete from Users where UserName = \'{0}\''.format(username)

def get_group_names():
    return 'select GroupName from radgroupcheck where id < 5'

def get_areas():
    return 'select Area from Areas'

def insert_new_user(data):
    user, name, pwd, area, idn, email, address, phone, notes, group, auth = data
    return '''insert into Users (UserName, Name, Password, Area, id, email, address, phone, notes, GroupName, autorizo_hasta)
                values (\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\', \'{6}\', \'{7}\', \'{8}\', \'{9}\', \'{10}\')'''\
                .format(user, name, pwd, area, idn, email, address, phone, notes, group, auth)

def insert_into_dbroles(user, rol):
    return 'insert into DBRoles (username, roles) values (\'{0}\', \'{1}\')'.format(user, rol)

def update_rol(user, rol):
    return 'update DBRoles set roles = \'{0}\' where username = \'{1}\''.format(rol, user)

def get_pendings():
    return 'select * from Pending'