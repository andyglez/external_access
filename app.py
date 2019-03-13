from flask import Flask, render_template, request, redirect, url_for, flash
from os import urandom
from settings import database as db

app = Flask(__name__)
app.secret_key = str(urandom(24))

db.query(db.create_db_roles, False)
db.query(db.create_pending, False)
if len(db.query('select * from DBRoles')) == 0:
    db.query(db.insert_roles)
if __name__ == '__main__':    
    app.run(debug=True, host='0.0.0.0', port=5000)


@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'GET':
        return render_template('login.html')
    data = db.query('select UserName, Password from Users where Username=\'' + request.form['user']+'\' and Password=\'' + request.form['password']+ '\'')
    if len(data) == 0:
        flash('Incorrect User Name or Password')
        return redirect(url_for('start'))
    usr, pwd = data[0]
    result, _ = db.query('select roles, username from DBRoles where UserName = \'' + usr + '\'')[0]
    roles = result.split(',')
    return index(usr, roles)

@app.route('/index', methods=['GET', 'POST'])
def index(username, roles):
    return 'I\'m at index'

@app.route('/request', methods=['GET', 'POST'])
def request_form():
    if request.method == 'GET':
        return render_template('request.html')
    return ''

