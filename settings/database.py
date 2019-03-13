#Configuration file that contains every needed setting for project extensibility and support
#There are presented some default examples and explanations about what the field is about

import MySQLdb

#-------------------------- MySQL Database Settings ------------------------
# Made for connections through a mySQL database server
host = 'tesis.home.cu'
user = 'radius'
pwrd = 'holamundo'
dbse = 'radius'
kargs = dict(use_unicode=1, connect_timeout=10)

get_connection = MySQLdb.Connection(*(host, user, pwrd, dbse), **kargs)

def query(s, is_select=True):
    cursor = get_connection.cursor()
    cursor.execute(s)
    lst = [i for i in cursor.fetchall()] if is_select else []
    cursor.close()
    get_connection.commit()
    return lst
#---------------------------------------------------------------------

#--------------------------- DB Requirements -------------------------
# Creation of tables and data required for administration purposes

# Table creation
create_db_roles = '''create table if not exists DBRoles(
                        entry_id int auto_increment,
                        username varchar(255) not null,
                        roles varchar(255) not null,
                        primary key(entry_id)
                        ) Engine=innodb'''

create_pending = '''create table if not exists Pending(
                        username varchar(255) not null,
                        name varchar(255) not null,
                        password varchar(255),
                        phone varchar(100) not null,
                        primary key(username)
                        ) Engine=innodb'''

# Data insertion
insert_roles = '''insert into DBRoles (username, roles)
                select UserName, \'default\' 
                from Users'''
