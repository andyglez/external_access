#Configuration file that contains every needed setting for project extensibility and support
#There are presented some default examples and explanations about what the field is about

import MySQLdb

#-------------------------- MySQL Database Settings ------------------------
# Made for connections through a mySQL database server
host = '192.168.5.27'
user = 'radius'
pwrd = 'holamundo'
dbse = 'radius'
kargs = dict(use_unicode=1, connect_timeout=10)

def get_connection():
    return MySQLdb.Connection(*(host, user, pwrd, dbse), **kargs)

def query(s, is_select=True):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(s)
    lst = [[i for i in row] for row in cursor.fetchall()] if is_select else []
    cursor.close()
    conn.commit()
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
                        email varchar(255) not null,
                        name varchar(255) not null,
                        password varchar(255),
                        phone varchar(100) not null,
                        primary key(username)
                        ) Engine=innodb'''

create_removed_acct = '''create table if not exists RemovedUsers(
                            entry_id int auto_increment,
                            username varchar(255) not null,
                            name varchar(255) not null,
                            area varchar(100) not null,
                            removed_by varchar(255) not null,
                            reason varchar(255),
                            primary key(entry_id)
                            ) Engine=innodb'''
# Data insertion
insert_roles = '''insert into DBRoles (username, roles)
                select UserName, \'default\' 
                from Users'''


def initial_setup():
    query(create_db_roles, False)
    query(create_pending, False)
    query(create_removed_acct, False)
    if len(query('select * from DBRoles')) == 0:
        query(insert_roles)