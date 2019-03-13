def get_user(username, password):
    return '''select UserName, Password, GroupName
                from Users 
                where Username= \'%s\' 
                and Password=\'%s\'''' % username, password

def get_roles(username):
    return '''select roles, username
                from DBRoles
                where username= \'%s\'''' % username

def get_quota(groupname):
    return '''select Value 
            from radgroupcheck
            where GroupName = \'%s\'''' % groupname