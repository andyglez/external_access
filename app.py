from flask import Flask, render_template, request, redirect, url_for, flash, session
from languages import messages as msg
from languages.interface import get_words
from utils import query_builder as qb
from utils.cookies import Cookies
from os import urandom
from settings import database as db
from utils import userinfo, time_conversion
from datetime import datetime

app = Flask(__name__)
app.secret_key = str(urandom(24))

db.initial_setup()
cookies = Cookies(session)
if __name__ == '__main__':    
    app.run(debug=True, host='0.0.0.0', port=5000)


@app.route('/', methods=['GET', 'POST'])
def start():
    cookies.set('current', 'start')
    if not cookies.contains('lang'):
        cookies.set('lang', 'es')
    if request.method == 'GET':
        return render_template('login.html', word=get_words)
    if 'language' in request.form:
        cookies.set('lang', request.form['language'])
        return redirect(url_for('start'))
    data = db.query(qb.get_user(request.form['user'], request.form['password']))
    if len(data) == 0:
        flash(msg.wrong_user_pass(cookies.get('lang')), category='error')
        return redirect(url_for('start'))
    load_user_data(*data[0])
    return redirect(url_for('index'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    cookies.reset_all_flags(excepted='show_details')
    cookies.set('current', 'index')
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    if not cookies.contains('show_details'):
        cookies.set('show_details', False)
    if request.method == 'POST':
        cookies.set('show_details', not cookies.get('show_details'))
    return render_template('self_usage.html',
            word= get_words,
            len= lambda x: len(x),
            seconds_to_time=lambda x: time_conversion.seconds_to_time(x),
            percent = session['consumed'] * 100 / session['quota']['total'],
            showing_details = cookies.get('show_details'))

@app.route('/request', methods=['GET', 'POST'])
def request_form():
    cookies.set('current', 'request_form')
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
    cookies.clear_all()
    flash(msg.logout_successful(session['lang']))
    return redirect(url_for('start'))


@app.route('/profile/<user>', methods=['GET', 'POST'])
def profile(user):
    cookies.reset_all_flags('modify')
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    if not cookies.contains('modify'):
        cookies.set('modify', False)
    info = get_info(user)
    if request.method == 'POST':
        if 'old_password' in request.form and checked(request.form, info[-1]):
            db.query(qb.update_password(user, request.form['new_password']))
        cookies.set('modify', not cookies.get('modify'))
        return redirect(url_for('profile', user=user))
    return render_template('profile.html', 
                    word=get_words, 
                    data=info,
                    mod_pwd=cookies.get('modify'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    cookies.reset_all_flags('query_sent')
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    if not cookies.contains('query_sent'):
        cookies.set('query_sent', False)
    if not cookies.contains('data'):
        cookies.set('data', [])
    data = ([(u, n, a) for u, n, a in db.query(qb.get_users()) if a == cookies.get('info')[2]] if cookies.get('roles')['is_dean'] else
           [(u, n, a) for u, n, a in db.query(qb.get_users()) if request.form['query'] in n.lower()]) if request.method == 'POST' else []
    cookies.set('query_sent', request.method == 'POST')
    return render_template('search.html',word=get_words, flag=cookies.get('query_sent'), data=data, len= lambda x: len(x))

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
    session['info'] = get_info(usr)
    quota = db.query(qb.get_quota(grp))
    bonus = db.query(qb.get_quota_bonus(usr))
    session['quota'] = userinfo.get_user_quota(quota, bonus)
    consumed = db.query(qb.get_acct_consumed(usr))
    session['consumed'] = sum([stp.timestamp() - stt.timestamp() for u, stt, stp, phone in consumed])
    session['details'] = [(phone, stt, stp, stp.timestamp() - stt.timestamp()) for u, stt, stp, phone in consumed]
    session['headers'] = [x for x in msg.get_headers(session['lang'])]

def get_info(user):
    return db.query(qb.get_profile_data(user))[0]

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

def checked(form, pwd):
    if form['old_password'] != pwd:
        flash(msg.bad_password(cookies.get('lang')))
        return False
    elif form['new_password'] != form['verify_password']:
        flash(msg.mismatch_new_password(cookies.get('lang')))
        return False
    return True
