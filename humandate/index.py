import datetime
from datetime import timedelta
import re
from itertools import repeat

days_long = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
days_short = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
days = days_long + days_short

months_long = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
months_short = ['jan', 'feb', 'march', 'april', 'may', 'june', 'july', 'aug', 'sept', 'oct', 'nov', 'dec']
months = months_long + months_short

years = list(map(str, range(datetime.datetime.now().year - 50, datetime.datetime.now().year + 50)))

postfixes = {
    'h': 'hour',
    'm': 'minute',
    'd': 'day',
}

time_prefix = 'at'
time_postfix = ['am', 'pm']
day_postfix = 'th'

multipliers = {
    'second': ('seconds', 1),
    'minute': ('minutes', 1),
    'hour': ('hours', 1),
    'day': ('days', 1),
    'week': ('days', 7),
    'fortnight': ('days', 14),
    'month': ('days', 30),
    'year': ('days', 365),
}

direction = {
    'ago': -1,
    'last': -1,
    'past': -1,
}

transformations = dict(zip((x + 's' for x in multipliers.keys()), multipliers.keys()))
transformations.update({ 'next': '1', 'upcoming': '1', 'following': '1', 'a': '1', 'an': '1' })
transformations.update(dict(zip(direction.keys(), (x + ' ' + '1' for x in direction.keys()))))

keywords = list(multipliers.keys()) + months + months_short + years + days + days_short + list(direction.keys()) + [time_prefix] + time_postfix

text = '12 jan 2019 at 12 will be amazing'

def tokenize(string):
    pattern = re.compile(r'\b(' + '|'.join(transformations.keys()) + r')\b')
    string = pattern.sub(lambda x: transformations[x.group()], string)

    words = string.lower().split(' ')
    n = len(words)
    filtered = []
    for (i, w) in enumerate(words):
        if w in keywords:
            filtered.append(w)
        elif w.isdigit() and ((i + 1 < n and words[i + 1] in keywords) or (i > 0 and words[i - 1] == time_prefix)):
            filtered.append(int(w))
        elif w[0:-1].isdigit():
            postfix = next((x for x in postfixes if w.endswith(x)), None)
            if postfix is not None:
                filtered.append(int(w[0:-1]))
                filtered.append(postfixes[postfix])
        elif w[0:-2].isdigit() and w[-2:] in time_postfix and int(w[0:-2]) <= 12:
            filtered.append(int(w[0:-2]))
            filtered.append(w[-2:])
        elif w[0:-2].isdigit() and w[-2:] == day_postfix:
            filtered.append(int(w[0:-2]))
            filtered.append(day_postfix)
        elif ':' in w:
            f, s = w[0:w.index(':')], w[w.index(':') + 1:]

            if f.isdigit() and s.isdigit() and int(f) < 24 and int(s) < 60:
                filtered.append((int(f), int(s)))

    return filtered

def compute(tokens):
    base = datetime.datetime.now()
    value = timedelta(0)
    month = None
    weekday = None
    day = None
    year = None
    time = None
    cdir = 1
    n = len(tokens)

    for (i, t) in enumerate(tokens):
        has_next = i + 1 < n

        if t in direction:
            cdir = direction[t]
        elif isinstance(t, int) and has_next and tokens[i + 1] in multipliers:
            key, v = multipliers[tokens[i + 1]]
            value += timedelta(**{ key: t * v })
        elif isinstance(t, int) and has_next and (tokens[i + 1] in months or tokens[i + 1] == day_postfix):
            day = t
        elif isinstance(t, int) and has_next and tokens[i + 1] in time_postfix:
            if tokens[i + 1] == 'am':
                if t == 12:
                    time = datetime.time(0)
                else:
                    time = datetime.time(t)
            else:
                if t == 12:
                    time = datetime.time(12)
                else:
                    time = datetime.time(t + 12)

        elif t in months:
            month = months.index(t) % 12
        elif t in years:
            year = t
        elif t in days:
            weekday = days.index(t) % 7
        elif isinstance(t, tuple):
            f,s = t

            time = datetime.time(f, s)
        elif t == time_prefix and has_next and isinstance(tokens[i + 1], int) and tokens[i + 1] < 24:
            time = datetime.time(tokens[i + 1])
            tokens[i + 1] = None

    try:
        if time is not None:
            base = base.replace(hour=time.hour, minute=time.minute)
        if month is not None:
            base = base.replace(month=month + 1)
        if weekday is not None:
            td = None
            if weekday > base.weekday():
                td = timedelta(days=weekday - base.weekday())
            else:
                td = timedelta(days=weekday - base.weekday() + 7)

            if cdir == -1:
                td = timedelta(days=7) - td

            base += cdir * td
        if year is not None:
            base = base.replace(year=int(year))

        if day is not None:
            base = base.replace(day=day)
    except:
        pass

    return cdir * value + base

def parse_date(string):
    return compute(tokenize(string))
