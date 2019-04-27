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
from controllers import main, login, index_ctr, request_ctr, profile_ctr, search_ctr, remove_ctr, create_ctr, pending_ctr, logout_ctr

app = Flask(__name__)
app.secret_key = str(urandom(24))

main.init_app()
cookies = Cookies(session)


@app.route('/', methods=['GET', 'POST'])
def start():
    login.set_cookies(cookies)
    if request.method == 'GET':
        return render_template('login.html', word=get_words)
    if 'language' in request.form:
        cookies.set('lang', request.form['language'])
        return redirect(url_for('start'))
    value, message = login.check_user_login(request.form['user'], request.form['password'], cookies)
    if not value:
        flash(message, category='error')
        return redirect(url_for('start'))
    return redirect(url_for('index', user=cookies.get('user'), group=cookies.get('group'), page=1))

@app.route('/index?user=<user>&group=<group>&page=<page>', methods=['GET', 'POST'])
def index(user, group, page=1):
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    if user != cookies.get('user') and not (cookies.get('roles')['is_root'] or cookies.get('roles')['is_admin']):
        return redirect(url_for('index', user=cookies.get('user'), group=cookies.get('group'), page=1))
    index_ctr.set_cookies(cookies)
    phone = login.get_profile_data(user)[0][5]
    (regular, roaming) = index_ctr.set_data_to_cookies(user, group, phone, cookies)
    if request.method == 'POST':
        cookies.set('show_details', not cookies.get('show_details'))
    return render_template('self_usage.html', word= get_words, len= lambda x: len(x),
            seconds_to_time=lambda x: time_conversion.seconds_to_time(x),
            regular = regular, roaming = roaming, user = user, group = group, self_data=(user == cookies.get('user')),
            showing_details = cookies.get('show_details'), enumerate=lambda x: enumerate(x),
            in_page=lambda i: i >= (int(page) - 1) * 10 and i < int(page) * 10, current=int(page), total=total)

@app.route('/delete?user=<user>&phone=<phone>&consumed=<consumed>&group=<group>')
def delete(user, phone, consumed, group):
    index_ctr.delete_record(user, phone, consumed)
    return redirect(url_for('index', user=user, group=group)) 

@app.route('/request', methods=['GET', 'POST'])
def request_form():
    cookies.set('current', 'request_form')
    if request.method == 'GET':
        return render_template('request.html', word=get_words)
    value, message = request_ctr.is_a_valid_request(request.form['user'], request.form['email'], cookies.get('lang'))
    if not value:
        flash(message, category='error')
        return redirect(url_for('request_form'))
    request_ctr.make_request(request.form, cookies.get('lang'))
    return redirect(url_for('start'))

@app.route('/logout')
def logout():
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    flash(logout_ctr.clear_session(cookies))
    return redirect(url_for('start'))


@app.route('/profile/<user>', methods=['GET', 'POST'])
def profile(user):
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    profile_ctr.set_cookies(cookies)
    info = login.get_profile_data(user)[0]
    if profile_ctr.check_role_permissions(user, info, cookies):
        return redirect(url_for('index', user=cookies.get('user'), group=cookies.get('group'), page=1))
    (current, rest) = profile_ctr.current_roles(user)
    if request.method == 'POST':
        (flag, msg) = profile_ctr.save_profile_action(user, request.form, info[-1], cookies)
        if not msg == '':
            flash(msg)
        return redirect(url_for('profile', user=user))
    return render_template('profile.html', word=get_words, data=info, rol=current, roles=rest, user=user, group=login.get_basic_info(user)[0][-1],
                    is_modifyer=(info[0] == cookies.get('user') or not (cookies.get('roles')['is_dean'] or cookies.get('roles')['is_ddi'])),
                    mod_pwd=cookies.get('modify'))

@app.route('/search?category=<category>', methods=['GET', 'POST'])
def search_none(category='name'):
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    if search_ctr.dont_have_permissions(cookies.get('roles')):
        return redirect(url_for('index', user=cookies.get('user'), group=cookies.get('group'), page=1))
    if request.method == 'POST':
        if request.form['query'] == '':
            return redirect(url_for('search_none',category=category))
        return redirect(url_for('search', category=category, query=request.form['query'], page=1))
    return render_template('search.html', word=get_words, category=category, page=1)

@app.route('/search?category=<category>&query=<query>&page=<page>', methods=['GET', 'POST'])
def search(category, query='', page=1):
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    if search_ctr.dont_have_permissions(cookies.get('roles')):
        return redirect(url_for('index', user=cookies.get('user'), group=cookies.get('group'), page=1))
    if request.method == 'POST':
        return redirect(url_for('search', category=category, query=request.form['query'], page=str(page)))
    data = search_ctr.search(cookies, query, category)
    total = len(data) // 10 if len(data) % 10 == 0 else (len(data) // 10) + 1
    if int(page) > total and total > 0:
        return redirect(url_for('search', category=category, query=query, page=1))
    return render_template('search.html',word=get_words, flag=True, data=data, len= lambda x: len(x),
                            category=category, page=page, enumerate=lambda x:enumerate(x),
                            in_page=lambda i: i >= (int(page) - 1) * 10 and i < int(page) * 10,
                            current=int(page), total=total)

@app.route('/remove?user=<user>&name=<name>&area=<area>', methods=['GET', 'POST'])
def remove(user, name, area):
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    if remove_ctr.dont_have_permissions(cookies.get('roles')):
        return redirect(url_for('index', user=cookies.get('user'), group=cookies.get('group'), page=1))
    if request.method == 'POST' and 'reason' in request.form:
        remove_ctr.log_removal(user, name, area, cookies.get('user'), request.form['reason'])
        return redirect(url_for('search', query=cookies.get('query_value')))
    return render_template('delete.html', word=get_words)

@app.route('/create', methods=['GET', 'POST'])
def create_user():
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    if create_ctr.dont_have_permissions(cookies.get('roles')):
        return redirect(url_for('index', user=cookies.get('user'), group=cookies.get('group'), page=1))
    (groups, roles, areas) = create_ctr.load_visual_options()
    if request.method == 'POST':
        if len(login.get_profile_data(request.form['user'])) > 0:
            flash(create_ctr.duplicate_error(request.form['user'], cookies.get('lang')))
        else:
            flash(create_ctr.create_user(request.form, cookies.get('lang')))
    return render_template('create.html', word=get_words, group=groups, roles=roles, areas=areas)

@app.route('/pending')
def pending():
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    if pending_ctr.dont_have_permissions(cookies.get('roles')):
        return redirect(url_for('index', user=cookies.get('user'), group=cookies.get('group'), page=1))
    (data, headers) = pending_ctr.get_data()
    return render_template('pending.html', word=get_words, data=data, headers=headers, len=lambda x: len(x), enumerate=lambda x: enumerate(x))

if __name__ == '__main__':    
    app.run(debug=True, host='0.0.0.0', port=5000)