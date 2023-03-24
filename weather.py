import datetime

import geocoder
import requests

API_KEY = '81311e67a862c8655c4ac24601464bb3'
HOST = 'https://api.openweathermap.org/data/2.5/'
DAYS = [
    {'num': 0, 'title': 'понедельник', 'active': False, 'color': '#FFFFFF', 'order': [0, 1, 2, 3, 4, 5, 6], 'temp' : 0, 'type' : '-'},
    {'num': 1, 'title': 'понедельник', 'active': False, 'color': '#FFFFFF', 'order': [0, 1, 2, 3, 4, 5, 6], 'temp' : 0, 'type' : '-'},
    {'num': 2, 'title': 'понедельник', 'active': False, 'color': '#FFFFFF', 'order': [0, 1, 2, 3, 4, 5, 6], 'temp' : 0, 'type' : '-'},
    {'num': 3, 'title': 'понедельник', 'active': False, 'color': '#FFFFFF', 'order': [0, 1, 2, 3, 4, 5, 6], 'temp' : 0, 'type' : '-'},
    {'num': 4, 'title': 'понедельник', 'active': False, 'color': '#FFFFFF', 'order': [0, 1, 2, 3, 4, 5, 6], 'temp' : 0, 'type' : '-'},
    {'num': 5, 'title': 'понедельник', 'active': False, 'color': '#FFFFFF', 'order': [0, 1, 2, 3, 4, 5, 6], 'temp' : 0, 'type' : '-'},
    {'num': 6, 'title': 'понедельник', 'active': False, 'color': '#FFFFFF', 'order': [0, 1, 2, 3, 4, 5, 6], 'temp' : 0, 'type' : '-'},
]


def today():
    g = geocoder.ip('me')
    city = g.city
    lat = g.lat
    lon = g.lng

    print(city, lat, lon)

    req = requests.get(f'{HOST}weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&land=ru').json()
    res = {
        'city': req['name'],
        'dis': req['weather'][0]['description'],
        'temp': int(round(req['main']['temp'])),
        'fells': str(round(req['main']['feel_like'])) + ' C',
        'pressure': str(round(req['main']['pressure'] / 1000 * 750, 2)),
        'wind': req['wind'],
    }
    return res

def week():
    today = datetime.datetime.today()
    DAYS[today.weekday()]['active'] = True

    for i in DAYS:
        if DAYS[today.weekday()]['active']:
            order = DAYS[today.weekday()]['order']
    g = geocoder.ip('me')
    city = g.city
    lat = g.lat
    lon = g.lng

    req = requests.get(f'{HOST}onecall?/exclude=daily&lat={lat}&lon={lon}&appid={API_KEY}&units=metric&land=ru').json()
    res = [DAYS[i] for i in order]

    for i in req['daily']:
        index = req['daily'].index(1)
        if index == 7:
            break
        res[index]['temp'] = i['temp']['day']
        res[index]['type'] = i['weather'][0]['description']
    return res

today()
