from flask import Flask, render_template, request, redirect, url_for, flash, session
from languages import messages as msg
from languages.interface import get_words
from utils import query_builder as qb
from utils.cookies import Cookies
from os import urandom
from settings import database as db
from settings import encryption as cr
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
    data = db.query(qb.get_user(request.form['user']))
    if len(data) == 0 or not cr.check(request.form['password'], data[0][1]):
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
    quota = db.query(qb.get_quota(grp))
    bonus = db.query(qb.get_quota_bonus(usr))
    cookies.set('quota', userinfo.get_user_quota(quota, bonus))
    consumed = db.query(qb.get_acct_consumed(usr))
    cookies.set('consumed', sum([stp.timestamp() - stt.timestamp() for u, stt, stp, phone in consumed]))
    cookies.set('details', [(phone, stt, stp, stp.timestamp() - stt.timestamp()) for u, stt, stp, phone in consumed])
    if request.method == 'POST':
        cookies.set('show_details', not cookies.get('show_details'))
    return render_template('self_usage.html',
            word= get_words,
            len= lambda x: len(x),
            seconds_to_time=lambda x: time_conversion.seconds_to_time(x),
            percent = cookies.get('consumed') * 100 / cookies.get('quota')['total'],
            showing_details = cookies.get('show_details'))

@app.route('/request', methods=['GET', 'POST'])
def request_form():
    cookies.set('current', 'request_form')
    if request.method == 'GET':
        return render_template('request.html', word=get_words)
    if not is_a_valid_request(request.form['user'], request.form['phone']):
        return redirect(url_for('request_form'))
    full_name = request.form['name'] + ' ' + request.form['last_name']
    crypted = cr.encrypt(request.form['password'])
    db.query(qb.insert_into_pending(request.form['user'], fullname, crypted, request.form['phone']))
    flash(msg.request_sent_successfully(session['lang']))
    return redirect(url_for('start'))

@app.route('/logout')
def logout():
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    cookies.reset_all_flags()
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
    all_roles = ['root', 'admin', 'ddi', 'dean', 'default']
    if check_role_permissions(user, info):
        return redirect(url_for('index'))
    rol, _ = db.query(qb.get_roles(user))[0]
    roles = [x for x in all_roles if x != rol]
    if request.method == 'POST':
        if 'old_password' in request.form and checked(request.form, info[-1]):
            crypted = cr.encrypt(request.form['new_password'])
            db.query(qb.update_password(user, crypted))
            cookies.set('modify', not cookies.get('modify'))
        elif 'rol' in request.form:
            db.query(qb.update_rol(user, request.form['rol']))
        return redirect(url_for('profile', user=user))
    return render_template('profile.html', 
                    word=get_words, 
                    data=info,
                    is_modifyer=(info[0] == cookies.get('user') or (not cookies.get('roles')['is_dean'])),
                    mod_pwd=cookies.get('modify'),
                    rol=rol,
                    roles=roles)

@app.route('/search', methods=['GET', 'POST'])
def search_none():
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    if cookies.get('roles')['is_default']:
        return redirect(url_for('index'))
    if request.method == 'POST':
        if request.form['query'] == '':
            return redirect(url_for('search_none'))
        return redirect(url_for('search', query=request.form['query']))
    return render_template('search.html', word=get_words)

@app.route('/search?query=<query>', methods=['GET', 'POST'])
def search(query=''):
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    if cookies.get('roles')['is_default']:
        return redirect(url_for('index'))
    if request.method == 'POST':
        return redirect(url_for('search', query=request.form['query']))
    
    data = ([(u, n, a) for u, n, a in db.query(qb.get_users()) if query in n.lower() and a == cookies.get('info')[2]] 
            if cookies.get('roles')['is_dean'] 
            else [(u, n, a) for u, n, a in db.query(qb.get_users()) if query in n.lower()])
    cookies.set('query_value', query)
    return render_template('search.html',word=get_words, flag=True, data=data, len= lambda x: len(x))

@app.route('/remove?user=<user>&name=<name>&area=<area>', methods=['GET', 'POST'])
def remove(user, name, area):
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    if not (cookies.get('roles')['is_dean'] or cookies.get('roles')['is_root']):
        return redirect(url_for('index'))
    if request.method == 'POST' and 'reason' in request.form:
        db.query(qb.insert_removed_user(user, name, area, cookies.get('user'), request.form['reason']), False)
        db.query(qb.delete_users(user))
        return redirect(url_for('search', query=cookies.get('query_value')))
    return render_template('delete.html', word=get_words)

@app.route('/create', methods=['GET', 'POST'])
def create_user():
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    if not cookies.get('roles')['is_root']:
        return redirect(url_for('index'))
    groups = [x[0] for x in db.query(qb.get_group_names())]
    roles = ['root', 'admin', 'ddi', 'dean', 'default']
    areas = [x[0] for x in db.query(qb.get_areas())]
    if request.method == 'POST':
        if len(get_info(request.form['user'])) > 0:
            flash(msg.user_already_exists(request.form['user'], session['lang']))
        else:
            form = request.form
            crypted = cr.encrypt(form['pass'])
            data = (form['user'], form['name'], crypted, form['area'],
                    form['id'], form['email'], form['address'], form['phone'],
                    form['notes'], form['group'], form['authorized'] if form['authorized'] else datetime.today().isoformat())
            db.query(qb.insert_new_user(data))
            db.query(qb.insert_into_dbroles(form['user'], form['roles']))
            flash(msg.user_creation_successfull(session['lang']))
    return render_template('create.html', word=get_words, group=groups, roles=roles, areas=areas)

@app.route('/pending')
def pending():
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    if not cookies.get('roles')['is_root']:
        return redirect(url_for('index'))
    data = db.query(qb.get_pendings())
    print(data)
    headers = [x[0] for x in db.query('show columns in Pending') if x[0] != 'password']
    return render_template('pending.html', word=get_words, data=data, headers=headers, len=lambda x: len(x))
    
def load_user_data(usr, pwd, grp):
    result, _ = db.query(qb.get_roles(usr))[0]
    session['user'] = usr
    session['roles'] = userinfo.get_user_roles(result.split(','))
    session['info'] = get_info(usr)
    session['headers'] = [x for x in msg.get_headers(session['lang'])]

def get_info(user):
    v = db.query(qb.get_profile_data(user))
    return v[0] if len(v) > 0 else v

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
    if cr.encrypt(form['old_password']) != pwd:
        flash(msg.bad_password(cookies.get('lang')))
        return False
    elif form['new_password'] != form['verify_password']:
        flash(msg.mismatch_new_password(cookies.get('lang')))
        return False
    return True

def check_role_permissions(user, info):
    if user != cookies.get('user') and cookies.get('roles')['is_default']:
        return True
    if len(info) == 0:
        return True
    if user != cookies.get('user') and cookies.get('roles')['is_dean'] and cookies.get('info')[2] != info[2]:
        return True
    return False