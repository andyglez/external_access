from flask import Flask, render_template, request, redirect, url_for, flash, session
from utils import query_builder as qb
from utils import messages as msg
from os import urandom
from settings import database as db
from utils import userinfo

app = Flask(__name__)
app.secret_key = str(urandom(24))

db.initial_setup()
if __name__ == '__main__':    
    app.run(debug=True, host='0.0.0.0', port=5000)


@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'GET':
        return render_template('login.html')
    data = db.query(qb.get_user(request.form['user'], request.form['password']))
    if len(data) == 0:
        flash(msg.wrong_user_pass(), category='error')
        return redirect(url_for('start'))
    load_user_data(*data[0])
    return redirect(url_for('index'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/request', methods=['GET', 'POST'])
def request_form():
    if request.method == 'GET':
        return render_template('request.html')
    if not is_a_valid_request(request.form['user'], request.form['phone']):
        return redirect(url_for('request_form'))
    full_name = request.form['name'] + ' ' + request.form['last_name']
    db.query(qb.insert_into_pending(request.form['user'], fullname, request.form['password'], request.form['phone']))
    flash(msg.request_sent_successfully())
    return redirect(url_for('start'))

@app.route('/logout')
def logout():
    if 'user' in session:
        session['user'] = ''
    if 'roles' in session:
        session['roles'] = {}
    return render_template('login.html')


def load_user_data(usr, pwd, grp):
    result, _ = db.query(qb.get_roles(usr))[0]
    session['user'] = usr
    session['roles'] = userinfo.get_user_roles(result.split(','))
    quota = db.query(qb.get_quota(grp))
    bonus = db.query(qb.get_quota_bonus(usr))
    session['quota'] = userinfo.get_user_quota(quota, bonus)

def is_a_valid_request(username, phone):
    data = db.query(qb.check_existance(username))
    if len(data) > 0:
        flash(msg.user_already_exists(username), category='error')
        return False
    data = db.query(qb.check_phone(phone))
    if len(data) > 0:
        flash(msg.phone_already_in_use())
        return False
    return True