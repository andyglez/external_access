from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from flask_mail import Mail
from languages import messages as msg
from languages.interface import get_words
from utils import query_builder as qb
from utils.cookies import Cookies
import os
from settings import database as db
from settings import encryption as cr
from utils import userinfo, time_conversion
from datetime import datetime
from controllers import main, login, index_ctr, request_ctr, profile_ctr, search_ctr, remove_ctr, create_ctr, pending_ctr, logout_ctr, authorize_ctr, password_ctr
import pdfkit

app = Flask(__name__)
app.secret_key = str(os.urandom(24))

main.init_app(app)
cookies = Cookies(session)
mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def start():
    if cookies.contains('user'):
        return redirect(url_for('index', user=cookies.get('user'), group=cookies.get('group'), page=1,
                        month=datetime.now().month, year=datetime.now().year))
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
    return redirect(url_for('index', user=cookies.get('user'), group=cookies.get('group'), page=1,
                        month=datetime.now().month, year=datetime.now().year))

@app.route('/index?user=<user>&group=<group>&page=<page>&month=<int:month>&year=<int:year>', methods=['GET', 'POST'])
def index(user, group, page=1, month=datetime.now().month, year=datetime.now().year):
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    if user != cookies.get('user') and not (cookies.get('roles')['is_root'] or cookies.get('roles')['is_admin'] or cookies.get('roles')['is_ddi']):
        return redirect(url_for('index', user=cookies.get('user'), group=cookies.get('group'), page=1), month, year)
    index_ctr.set_cookies(cookies)
    phone = login.get_profile_data(user)[0][5]
    (regular, roaming) = index_ctr.set_data_to_cookies(user, group, phone, cookies, month, year)
    if request.method == 'POST':
        if 'month' in request.form:
            return redirect(url_for('index', user=user, group=group, page=1,
                    month=time_conversion.month_to_int(request.form['month'].split()[0]),
                    year=int(request.form['month'].split()[1])))
        cookies.set('show_details', not cookies.get('show_details'))
    total = len(cookies.get('details')) // 10 if len(cookies.get('details')) % 10 == 0 else (len(cookies.get('details')) // 10) + 1
    data = index_ctr.get_bonus_logs(user)
    if int(page) > total and total > 0:
        return redirect(url_for('index', user=user, group=group, page=1, month=month, year=year))
    return render_template('self_usage.html', word= get_words, len= lambda x: len(x),
            seconds_to_time=lambda x: time_conversion.seconds_to_time(x),
            regular = regular, roaming = roaming, user = user, group = group, self_data=(user == cookies.get('user')),
            showing_details = cookies.get('show_details'), enumerate=lambda x: enumerate(x), to_date=month==cookies.get('month') and year==cookies.get('year'),
            in_page=lambda i: i >= (int(page) - 1) * 10 and i < int(page) * 10, current=int(page), total=total, data=data, mth=month, yr=year,
            clean_date= lambda x: x.date(), months=time_conversion.get_first_previous(year, month, 12), get_month=lambda x: time_conversion.int_to_month(x))

@app.route('/request', methods=['GET', 'POST'])
def request_form():
    cookies.set('current', 'request_form')
    if not cookies.contains('show_req'):
        cookies.set('show_req', False)
    if request.method == 'GET':
        return render_template('request.html', word=get_words,
        data=cookies.get('request') if cookies.get('show_req') else {},
        show=cookies.get('show_req'))
    value, message = request_ctr.is_a_valid_request(request.form, cookies.get('lang'))
    if not value:
        flash(message, category='error')
        cookies.set('request', request.form)
        cookies.set('show_req', True)
        return redirect(url_for('request_form'))
    resp = request_ctr.make_request(request.form['user'], mail, request.form, cookies.get('lang'))
    flash(resp)
    cookies.set('show_req', False)
    return redirect(url_for('start'))

@app.route('/request?new_password', methods=['GET', 'POST'])
def request_password():
    if request.method == 'GET':
        return render_template('password.html', word=get_words, confirm=False)
    value, message = password_ctr.check_info(request.form['email'], mail, cookies.get('lang'))
    flash(message)
    return redirect(url_for('request_password'))
    
@app.route('/request?new_password&user=<user>&dni=<dni>&e_addr=<e_addr>', methods=['GET', 'POST'])
def confirm_password(user,dni, e_addr):
    if request.method == 'GET':
        return render_template('password.html', word=get_words, confirm=True, user=user, e_addr=e_addr)    
    value, message = password_ctr.verify_email(user, request.form['pass'], request.form['conf'], cookies.get('lang'))
    flash(message)
    if value:
        return redirect(url_for('start'))
    return redirect(url_for('confirm_password', user, dni, e_addr))   

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
        return redirect(url_for('index', user=cookies.get('user'), group=cookies.get('group'), page=1,
                        month=datetime.now().month, year=datetime.now().year))
    (current, rest) = profile_ctr.current_roles(user)
    if request.method == 'POST':
        if 'bonus' in request.form:
            if request.form['until'] != '' and request.form['comment'] != '':
                d = datetime.strptime(request.form['until'], '%Y-%m-%d')
                if request.form['bonus'].isnumeric() and int(request.form['bonus']) > 0 and d > datetime.today():
                    seconds = time_conversion.hours_to_seconds(int(request.form['bonus']))
                    profile_ctr.add_quota_bonus(user, seconds, request.form['comment'], request.form['until'])
                else:
                    flash('error')
            else:
                flash('error')
            return redirect(url_for('profile', user=user))
        flags = Cookies(cookies.get('is_field_mod'))
        profile_ctr.set_flags(flags, request.form)
        if profile_ctr.execute_if_modification(user, flags, request.form):
            return redirect(url_for('profile', user=user))
        (flag, msg) = profile_ctr.save_profile_action(user, request.form, info[-1], cookies)
        if not msg == '':
            flash(msg)
        return redirect(url_for('profile', user=user))
    info[2] = db.query('select areaname from Areas where area = \'{0}\''.format(info[2]))[0][0]
    return render_template('profile.html', word=get_words, data=info, rol=current, roles=rest, user=user, group=login.get_basic_info(user)[0][-1],
                    is_modifyer=(info[0] == cookies.get('user') or not (cookies.get('roles')['is_dean'] or cookies.get('roles')['is_ddi'])),
                    mod_pwd=cookies.get('modify'), flags=cookies.get('is_field_mod'))

@app.route('/search?category=<category>', methods=['GET', 'POST'])
def search_none(category='name'):
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    if search_ctr.dont_have_permissions(cookies.get('roles')):
        return redirect(url_for('index', user=cookies.get('user'), group=cookies.get('group'), page=1,
                                month=datetime.now().month, year=datetime.now().year))
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
        return redirect(url_for('index', user=cookies.get('user'), group=cookies.get('group'), page=1,
                        month=datetime.now().month, year=datetime.now().year))
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

@app.route('/remove?user=<user>&name=<name>&area=<area>&category=<category>&page=<page>', methods=['GET', 'POST'])
def remove(user, name, area, category, page):
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    if remove_ctr.dont_have_permissions(cookies.get('roles')):
        return redirect(url_for('index', user=cookies.get('user'), group=cookies.get('group'), page=1,
                        month=datetime.now().month, year=datetime.now().year))
    if request.method == 'POST' and 'reason' in request.form:
        remove_ctr.log_removal(user, name, area, cookies.get('user'), request.form['reason'])
        return redirect(url_for('search', category=category, query=cookies.get('query_value'), page=page))
    return render_template('delete.html', word=get_words)

@app.route('/create', methods=['GET', 'POST'])
def create_user():
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    if create_ctr.dont_have_permissions(cookies.get('roles')):
        return redirect(url_for('index', user=cookies.get('user'), group=cookies.get('group'), page=1,
                        month=datetime.now().month, year=datetime.now().year))
    (groups, roles, areas) = create_ctr.load_visual_options()
    if request.method == 'POST':
        if len(login.get_profile_data(request.form['user'])) > 0:
            flash(create_ctr.duplicate_error(request.form['user'], cookies.get('lang')))
        else:
            flash(create_ctr.create_user(request.form, cookies.get('lang')))
    return render_template('create.html', word=get_words, group=groups, roles=roles, areas=areas)

@app.route('/pending?page=<page>')
def pending(page=1):
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    if pending_ctr.dont_have_permissions(cookies.get('roles')):
        return redirect(url_for('index', user=cookies.get('user'), group=cookies.get('group'), page=1,
                        month=datetime.now().month, year=datetime.now().year))
    (data, headers) = pending_ctr.get_data()
    flags = [x[-1] == '' for x in data]
    total = len(data) // 10 if len(data) % 10 == 0 else (len(data) // 10) + 1
    if cookies.get('roles')['is_dean']:
        data = [x for x in data if x[3] == cookies.get('area')]
    if int(page) > total and total > 0:
        return redirect(url_for('pending', page=1))
    return render_template('pending.html', word=get_words, data=data, headers=headers, len=lambda x: len(x), enumerate=lambda x: enumerate(x),
                            in_page=lambda i: i >= (int(page) - 1) * 10 and i < int(page) * 10,current=int(page), total=total, flags=flags,
                            clean_date=lambda x: x.split('T')[0])

@app.route('/authorize?username=<username>&ident=<dni>&authorized_by=<author>&action=<action>')
def authorize(username, dni, author, action):
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    if action == 'dean':
        authorize_ctr.authorize_dean_action(username, cookies.get('user'), mail)
        flash(msg.request_sent_successfully(cookies.get('lang')))
        return redirect(url_for('pending', page=1))
    if not authorize_ctr.check_pending(username, dni, author):
        flash('Error')
        return redirect(url_for('pending', page=1))
    authorize_ctr.update_auth(username, dni, author, mail)
    flash(msg.request_sent_successfully(cookies.get('lang')))
    return redirect(url_for('pending', page=1))

@app.route('/pdf/<username>&<name>&<dni>&<phone>&<e_mail>')
def render_pdf(username, name, dni, phone, e_mail):
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    data = userinfo.consume_webservice(e_mail)
    author = cookies.get('info')[1]
    rendered = render_template('pdf_template.html', 
                                user=username, name=name, dni=dni, phone=phone, e_mail=e_mail,
                                year=datetime.now().year, cat=data.CatDocenteInvestigativa,
                                ocp=data.CatOcupacional, author=author)
    pdf = pdfkit.from_string(rendered, False, css=os.path.dirname(os.path.abspath(__file__)) + url_for('static', filename='css/print.css'))
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=Acceso-Remoto-{0}.pdf'.format(name)
    return response

@app.route('/dismiss?username=<username>')
def dismiss(username):
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    db.query('delete from Pending where username = \'{0}\''.format(username))
    return redirect(url_for('pending', page=1))

@app.route('/remove_bonus?user=<user>&bonus=<bonus>&comment=<comment>&group=<group>&page=<page>&month=<month>&year=<year>')
def remove_bonus(user, bonus, comment, group, page, month, year):
    if not cookies.contains('user'):
        return redirect(url_for('start'))
    db.query('delete from QuotaBonus where UserName = \'{0}\' and Bonus = \'{1}\' and Comment = \'{2}\''.format(user, bonus, comment))
    return redirect(url_for('index', user=user, group=group, page=page, month=month, year=year))

if __name__ == '__main__':    
    app.run(debug=True, host='0.0.0.0', port=5000)