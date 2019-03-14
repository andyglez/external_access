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
    return '''select Bonus,UserName
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

def get_acct_consumed(username):
    return '''select UserName,AcctStartTime,AcctStopTime
                from radacct
                where UserName = \'{0}\'
                and AcctStartTime >= \'{1}\'
                and AcctStartTime <= \'{2}\''''.format(username
                ,datetime(datetime.now().year, datetime.now().month, datetime.now().day)
                ,datetime(datetime.now().year, datetime.now().month, datetime.now().day + 1))