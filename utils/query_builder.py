from datetime import datetime

def get_user(username, password):
    return '''select UserName, Password, GroupName
                from Users 
                where Username= \'{0}\' 
                and Password=\'{1}\''''.format(username, password)

def get_roles(username):
    return '''select roles, username
                from DBRoles
                where username= \'{0}\''''.format(username)

def get_quota(groupname):
    return '''select Value, GroupName
            from radgroupcheck
            where GroupName = \'{}\''''.format(groupname)

def get_quota_bonus(username):
    return '''select Bonus
            from QuotaBonus
            where UserName = \'{0}\'
            and Expires > \'{1}\''''.format(username, datetime.now())

def check_existance(username):
    return 'select * from Users where Username=\'{}\''.format(username)

def check_phone(phone):
    return 'select * from Pending where phone=\'{}\''.format(phone)

def insert_into_pending(username, fullname, password, phone):
    return '''insert into Pending (username, name, password, phone)
            values(\'{0}\',\'{1}\',\'{2}\',\'{3}\')'''.format(username, fullname, password, phone)