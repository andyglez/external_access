from utils.cookies import Cookies
from utils import userinfo
from settings import database as db
from datetime import datetime

def set_cookies(cookies):
    cookies.reset_all_flags(excepted='show_details')
    cookies.set('current', 'index')
    if not cookies.contains('show_details'):
        cookies.set('show_details', False)

def set_data_to_cookies(cookies):
    data = build_data_from_user_quota(cookies.get('user'), cookies.get('group'), cookies.get('phone'))
    (quota, regular_consumed, roaming_consumed, details, perc_regular, perc_roam) = data
    cookies.set('quota', quota)
    cookies.set('consumed', regular_consumed)
    cookies.set('roaming', roaming_consumed)
    cookies.set('details', details)
    return (perc_regular, perc_roam)

def build_data_from_user_quota(user, group, phone):
    quota = get_quota(group)
    bonus = get_bonus(user)
    quota = userinfo.get_user_quota(quota, bonus)
    consumed = get_consumed(user)
    regular_consumed = sum([b.timestamp() - a.timestamp() for u, a, b, p in consumed if p in phone])
    roaming_consumed = sum([b.timestamp() - a.timestamp() for u, a, b, p in consumed if p not in phone])
    details = [(p, stt, stp, stp.timestamp() - stt.timestamp()) for u, stt, stp, p in consumed]
    return (quota, regular_consumed, roaming_consumed, details, regular_consumed * 100 / quota['total'], roaming_consumed * 100 / quota['roaming'])

def get_quota(groupname):
    return db.query('''select Value, GroupName
                        from radgroupcheck
                        where GroupName = \'{}\''''.format(groupname))

def get_bonus(username):
    return db.query('''select Bonus,UserName
                        from QuotaBonus
                        where UserName = \'{0}\'
                        and date_format(Expires, "%Y-%m-%d") > \'{1}\''''.format(username, datetime.now().date().isoformat()))

def get_consumed(username):
    return db.query('''select UserName,AcctStartTime,AcctStopTime,CallingStationId
                        from radacct
                        where UserName = \'{0}\'
                        and date_format(AcctStartTime, "%Y-%m-%d") >= \'{1}\'
                        and date_format(AcctStopTime, "%Y-%m-%d") < \'{2}\''''.format(username
                        ,datetime(datetime.now().year, datetime.now().month, 1).date().isoformat()
                        ,datetime(datetime.now().year, datetime.now().month, datetime.now().day + 1).date().isoformat()))