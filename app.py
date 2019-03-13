from flask import Flask, render_template, request, redirect, url_for, flash, session
from os import urandom
from settings import database as db
from utils import userinfo

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
        flash('Nombre de usuario o contraseña incorrectos', category='error')
        return redirect(url_for('start'))
    usr, pwd = data[0]
    result, _ = db.query('select roles, username from DBRoles where UserName = \'' + usr + '\'')[0]
    session['roles'] = result.split(',')
    session['user'] = usr
    return redirect(url_for('index'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', is_root=userinfo.is_root(session['roles']))

@app.route('/request', methods=['GET', 'POST'])
def request_form():
    if request.method == 'GET':
        return render_template('request.html')
    data = db.query('select * from Users where Username=\'' + request.form['user'] + '\'')
    if len(data) > 0:
        flash('El usuario ' + request.form['user'] + ' ya existe', category='error')
        return redirect(url_for('request_form'))
    data = db.query('select * from Pending where phone=\'' + request.form['phone'] + '\'')
    if len(data) > 0:
        flash('El teléfono ' + request.form['phone'] + ' ya está anclado a otra cuenta')
        return redirect(url_for('request_form'))
    full_name = request.form['name'] + ' ' + request.form['last_name']
    db.query('insert into Pending (username, name, password, phone) ' + 
            'values(\'' + request.form['user'] + '\',\'' + full_name + '\',\'' + request.form['password'] + '\',\'' + request.form['phone'] + '\')')
    flash('Operación exitosa. Contacte con su administrador de red en un par de días')
    return redirect(url_for('start'))

@app.route('/logout')
def logout():
    if 'user' in session:
        session['user'] = ''
    if 'roles' in session:
        session['roles'] = []
    return render_template('login.html')
