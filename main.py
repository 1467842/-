from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import datetime as pt

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
my_user_id = os.environ["MY_USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

def get_mum(momday1, today, round, tempday):
    try:
        ym = 6
        mm_year = int(momday1.split("-")[0])
        mm_month = int(momday1.split("-")[1])
        mm_day = int(momday1.split("-")[2])
        momday = date(mm_year, mm_month, mm_day)
        sumdays = str(today.__sub__(momday)).split(" ")[0]
        days = int(int(sumdays) / round)
        TempDay = tempday * days
        delta = pt.timedelta(days=days * round + TempDay)
        startday = momday + delta
        delta = pt.timedelta(days=ym - 1)
        lastday = startday + delta
        if startday <= today <= lastday:
            if today != lastday:
                time1 = str(today.__sub__(startday))[0]
                mytext = '今天是第' + str(int(time1) + 1) + '天，还要坚持' + \
                         str(lastday.__sub__(today)).split(" ")[0] + '天哦'
            else:
                mytext = '今天是最后一天，明天就可以愉快地玩耍啦'
        else:
            a = int(str(lastday.__sub__(today)).split(" ")[0]) + 1
            if a <= 0:
                dy = 32 - ym - abs(a)
            else:
                dy = a - ym
            mytext = '还有' + str(dy) + '天到达战场'
    except:
        mytext = ''
    return mytext


def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['temp'])


def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


def get_birthday():
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
today_mum = datetime.date(datetime.now())
motertext = get_mum('2022-12-11', today_mum, 32, 1)
data = {"weather": {"value": wea}, "temperature": {"value": temperature}, "love_days": {"value": get_count()},
        "mum_days": {"value": motertext},
        "birthday_left": {"value": get_birthday()}, "words": {"value": get_words(), "color": get_random_color()}}
res = wm.send_template(my_user_id, template_id, data)
wm.send_template(user_id, template_id, data)
