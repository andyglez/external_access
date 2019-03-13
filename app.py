from flask import Flask, render_template, request, redirect, url_for, flash
from os import urandom
from settings import database as db

app = Flask(__name__)
app.secret_key = str(urandom(24))
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'GET':
        return render_template('login.html')
    data = query('select UserName, Password from Users where Username=\'' + request.form['user']+'\' and Password=\'' + request.form['password']+ '\'')
    if len(data) == 0:
        flash('Incorrect User Name or Password')
        return redirect(url_for('start'))
    usr, pwd = data[0]
    result, _ = query('select roles, username from DBRoles where UserName = \'' + usr + '\'')[0]
    roles = result.split(',')
    return index(usr, roles)

@app.route('/index', methods=['GET', 'POST'])
def index(username, roles):
    return 'I\'m at index'

@app.route('/request', methods=['GET', 'POST'])
def request_form():
    return ''

def query(s):
    cursor = db.get_connection.cursor()
    cursor.execute(s)
    lst = [i for i in cursor.fetchall()]
    cursor.close()
    db.get_connection.commit()
    return lst