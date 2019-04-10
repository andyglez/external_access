from utils.cookies import Cookies
from languages import messages as msg

def clear_session(cookies):
    cookies.reset_all_flags()
    cookies.clear_all()
    return msg.logout_successful(cookies.get('lang'))