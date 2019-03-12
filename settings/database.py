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
#---------------------------------------------------------------------
