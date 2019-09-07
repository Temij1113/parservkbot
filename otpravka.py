# -*- coding: utf-8 -*-
import config
import telebot
import requests
import csv
import json
import datetime
import time



#Без обновления не работает
URL = "https://api.telegram.org/bot" + config.token + "/"

proxies = {
    'https': 'socks5://3.212.104.192:3128'
}

def get_updates():
    url = URL + 'getupdates'
    r = requests.get(url, proxies=proxies, ).text
    print(r)
    header("HTTP/1.1 200 OK")
spis_is_id=[]

def take_post():
    all_posts = []
    domain='menalis'
    version=5.101
    ofset = 0
    token = '692153de692153de692153de2c694dec7966921692153de3452e2c6c6c9a8312d191b45'

    #запрос записей
    while ofset<1:
        res = requests.get('https://api.vk.com/method/wall.get',
                                params = {
                                'access_token':token,
                                'v':version,
                                'domain':domain,
                                'count':2,
                                'ofset':ofset
                                }

                                )
        data = res.json()['response']['items']
        all_posts.extend(data)
        return all_posts

def filter(all_posts):
    length = len(all_posts)
    filter_posts = []
    try:
        for post in all_posts:
            filter_post= {'id':'','text':'','url':'','type':''}
            for k,v in post.items():
                if k == 'id':
                    filter_post[k] = v
                elif k == 'text':
                    filter_post[k] = v
                elif k == 'attachments':
                    for p in v:
                        for q,w in p.items():
                            if q == 'photo':
                                for o,i in w.items():
                                    if o == 'sizes':
                                        for j in i:
                                            for u,y in j.items():
                                                if u == 'url':
                                                    filter_post[u]= y
                elif k == 'is_pinned':
                    filter_post["type"]= 'zakrep'
            filter_posts.append(filter_post)
        return filter_posts
    except UnicodeEncodeError :
        pass

def file_maker(filter_posts):
    FILE = 'posts.csv'
    columns = ["id", "text","url","type"]
    with open(FILE,'w',newline='',encoding="utf-8") as fl:
        posts = csv.DictWriter(fl,fieldnames = columns,extrasaction='ignore')
        posts.writeheader()
        posts.writerows(filter_posts)


def zag():
    FILE = 'posts.csv'
    with open(FILE, "r", newline="",encoding="utf-8") as file:
        with open('otp_zag.txt','r') as fl_z:
            reader = csv.DictReader(file)
            for row in reader:
                for stroka in fl_z.readlines():
                    if str(row["id"]) == str(stroka.strip()):
                        zagol=str(row["id"])
                        return zagol

def iskluch():
    FILE = 'posts.csv'
    with open(FILE, "r", newline="",encoding="utf-8") as file:
        with open('otp_post.txt','r') as fl_p:
            reader = csv.DictReader(file)
            for stroka in fl_p.readlines():
                for row in reader:
                    if str(row["id"]) == str(stroka.strip()):
                        nelizya=str(row["id"])
                        return nelizya

def otvet():
    FILE = 'posts.csv'
    print(1)
    all_posts = take_post()
    filter_posts = filter(all_posts)
    file_maker(filter_posts)
    zagol=zag()
    nelizya = iskluch()
    print(zagol)
    print(nelizya)
    with open(FILE, "r", newline="",encoding="utf-8") as file:
        with open('otp_zag.txt','r+') as fl_z:
            with open('otp_post.txt','r+') as fl_p:
                reader = csv.DictReader(file)
                for row in reader:
                    if str(row["id"]) != nelizya and str(row["id"]) != zagol:
                        if row["type"]== 'zakrep':
                            fl_z.write(str(row["id"]+"\n"))
                        elif row["type"]== '':
                            fl_p.write(str(row["id"]+"\n"))
                        bot.send_photo(-1001240055823,photo = row["url"],caption = row["text"] )
                        print(row)

bot = telebot.TeleBot(config.token)
vr = time.strftime("%H:%M",time.localtime())



@bot.message_handler(content_types=['text'])
def start_bot(message):
    if message.text.lower() == 'привет' and message.chat.id == 948488655 :
        bot.send_message(message.chat.id,'Привет,я работаю!)))Не волнуйся)')
    if message.text.lower() == 'ответ' and message.chat.id == 948488655 :
        otvet()

while True:
    all_posts = take_post()
    filter_posts = filter(all_posts)
    file_maker(filter_posts)
    otvet()
    zagol=zag()
    nelizya = iskluch()
    time.sleep(120)



if __name__ == '__main__':
    bot.polling(none_stop=True,timeout = 3.5)
