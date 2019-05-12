from settings import database as db
from utils.cookies import Cookies

def dont_have_permissions(roles):
    return roles['is_default']

def search(cookies, query, category):
    data = ([(u, n, a, e, p) for u, n, a, e, p in get_users(category) if by_category(query, category, u, n, a, e, p) and a == cookies.get('info')[2]] 
            if cookies.get('roles')['is_dean'] or cookies.get('roles')['is_admin']
            else [(u, n, a, e, p) for u, n, a, e, p in get_users(category) if by_category(query, category, u, n, a, e, p)])
    cookies.set('query_value', query)
    return data

def by_category(query, category, user, name, area, email, phone):
    if category == 'name':
        return query in name.lower()
    elif category == 'username':
        return query in user.lower()
    elif category == 'email':
        return query in email.lower()
    elif category == 'phone':
        return query in phone
    return query in area

def get_users(category):
    return db.query('select UserName, Name, Area, email, phone from Users order by {0}'.format(category))