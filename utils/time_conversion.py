months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

def month_to_int(month):
    for i,name in enumerate(months):
        if name == month:
            return i+1
    return None

def int_to_month(i):
    return months[i-1]

def seconds_to_time(total):
    seconds = total % 60
    minutes = (total/60) % 60
    hours = total / (60*60)
    return '%d:%.2d:%.2d' % (hours, minutes, seconds)

def previous_date(year, month):
    if month == 1:
        return (year-1, 12)
    return (year, month-1)

def next_date(year, month):
    if month == 12:
        return (year+1, 1)
    return (year, month+1)
