from flask import Flask, render_template, request, redirect, url_for, flash, session
from languages import messages as msg
from languages.interface import get_words
from utils import query_builder as qb
from os import urandom
from settings import database as db
from utils import userinfo, time_conversion
from datetime import datetime

app = Flask(__name__)
app.secret_key = str(urandom(24))

db.initial_setup()
if __name__ == '__main__':    
    app.run(debug=True, host='0.0.0.0', port=5000)


@app.route('/', methods=['GET', 'POST'])
def start():
    session['current'] = 'start'
    if 'lang' not in session:
        session['lang'] = 'es'
    if request.method == 'GET':
        return render_template('login.html', word=get_words)
    if 'language' in request.form:
        session['lang'] = request.form['language']
        return redirect(url_for('start'))
    data = db.query(qb.get_user(request.form['user'], request.form['password']))
    if len(data) == 0:
        flash(msg.wrong_user_pass(session['lang']), category='error')
        return redirect(url_for('start'))
    load_user_data(*data[0])
    return redirect(url_for('index'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'user' not in session:
        return render_template('login.html')
    session['current'] = 'index'
    if 'show_details' not in session:
        session['show_details'] = False
    if request.method == 'POST':
        session['show_details'] = not session['show_details']
    return render_template('self_usage.html',
            word= get_words,
            len= lambda x: len(x),
            seconds_to_time=lambda x: time_conversion.seconds_to_time(x),
            percent = session['consumed'] * 100 / session['quota']['total'],
            showing_details = request.method == 'POST')

@app.route('/request', methods=['GET', 'POST'])
def request_form():
    session['current'] = 'request_form'
    if request.method == 'GET':
        return render_template('request.html', word=get_words)
    if not is_a_valid_request(request.form['user'], request.form['phone']):
        return redirect(url_for('request_form'))
    full_name = request.form['name'] + ' ' + request.form['last_name']
    db.query(qb.insert_into_pending(request.form['user'], fullname, request.form['password'], request.form['phone']))
    flash(msg.request_sent_successfully(session['lang']))
    return redirect(url_for('start'))

@app.route('/logout')
def logout():
    session.pop('user')
    session.pop('roles')
    session.pop('show_details')
    session.pop('quota')
    session.pop('consumed')
    session.pop('details')
    session.pop('headers')
    return render_template('login.html')


@app.route('/profile')
def profile():
    return ''

@app.route('/es')
def es():
    session['lang'] = 'es'
    return redirect(url_for(session['current']))

@app.route('/en')
def en():
    session['lang'] = 'en'
    return redirect(url_for(session['current']))

@app.route('/ca')
def ca():
    session['lang'] = 'ca'
    return redirect(url_for(session['current']))

def load_user_data(usr, pwd, grp):
    result, _ = db.query(qb.get_roles(usr))[0]
    session['user'] = usr
    session['roles'] = userinfo.get_user_roles(result.split(','))
    quota = db.query(qb.get_quota(grp))
    bonus = db.query(qb.get_quota_bonus(usr))
    session['quota'] = userinfo.get_user_quota(quota, bonus)
    consumed = db.query(qb.get_acct_consumed(usr))
    session['consumed'] = sum([stp.timestamp() - stt.timestamp() for u, stt, stp, phone in consumed])
    session['details'] = [(phone, stt, stp, stp.timestamp() - stt.timestamp()) for u, stt, stp, phone in consumed]
    session['headers'] = [x for x in msg.get_headers(session['lang'])]

def is_a_valid_request(username, phone):
    data = db.query(qb.check_existance(username))
    if len(data) > 0:
        flash(msg.user_already_exists(username, session['lang']), category='error')
        return False
    data = db.query(qb.check_phone(phone))
    if len(data) > 0:
        flash(msg.phone_already_in_use(session['lang']))
        return False
    return True