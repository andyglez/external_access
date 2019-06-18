from utils.cookies import Cookies
from utils import userinfo
from settings import database as db
from datetime import datetime

def set_cookies(cookies):
    cookies.reset_all_flags(excepted='show_details')
    cookies.set('current', 'index')
    if not cookies.contains('show_details'):
        cookies.set('show_details', False)

def set_data_to_cookies(user, group, phone, cookies):
    data = build_data_from_user_quota(user, group, phone)
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
    regular_consumed = sum([b.timestamp() - a.timestamp() for u, a, b, p, i in consumed if p in phone and b.timestamp() > 0])
    roaming_consumed = sum([b.timestamp() - a.timestamp() for u, a, b, p, i in consumed if p not in phone and b.timestamp() > 0])
    details = [(i, p, stt, stp, stp.timestamp() - stt.timestamp() if stt.timestamp() > 0 else 0) for u, stt, stp, p, i in consumed]
    return (quota, regular_consumed, roaming_consumed, details, regular_consumed * 100 / quota['total'], roaming_consumed * 100 / quota['roaming'])


def get_bonus_logs(user):
    return db.query('''select Bonus,Comment,Expires
                        from QuotaBonus
                        where UserName = \'{0}\'
                        and date_format(Expires, "%Y-%m-%d") > \'{1}\''''.format(user, datetime.now().date().isoformat()))
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
    return db.query('''select UserName,AcctStartTime,AcctStopTime,CallingStationId,ConnectInfo_start
                        from radacct
                        where UserName = \'{0}@uh.cu\'
                        and date_format(AcctStartTime, "%Y-%m-%d") >= \'{1}\'
                        order by AcctStartTime desc'''.format(username
                        ,datetime(datetime.now().year, datetime.now().month, 1).date().isoformat()
                        ,datetime(datetime.now().year, datetime.now().month, 1).date().isoformat()                        
                        ,datetime(datetime.now().year, datetime.now().month, datetime.now().day + 1).date().isoformat()))