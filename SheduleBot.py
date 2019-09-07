import knocker
import vk_api
from bs4 import BeautifulSoup
# import curl
import requests
import datetime
import time
import os
import Farseer
import json


days = ['','']
def main(targetUrl: str):
    if targetUrl == "":
        url = "http://time-rtu.ru/?group=%D0%91%D0%91%D0%91%D0%9E-05-18"
    else:
        url = targetUrl
    headers = {'accept': "*/*", "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0", "referer": "http://time-rtu.ru/?group=%D0%91%D0%91%D0%91%D0%9E-05-18"}

    session = requests.Session()
    rawHtml = session.get(url=url, headers=headers)
    preParsedHtml = BeautifulSoup(rawHtml.content, "html.parser")
    i = 0
    for card in preParsedHtml.find_all('div', attrs={"id":"card"}):
        if i < 2:
            try:
                date = card.contents[1].text.replace("\n", '').replace(" ", '')
                days[i] += (date + "\n")
                print(date)
                for _lesson in card.contents[3].contents[1]:
                    if _lesson != "\n":
                        time = _lesson.contents[1].text.replace('\n', '').replace("                                                        ", '')
                        print(time)
                        days[i] += (time + "\n")
                        for lesson in _lesson.contents:
                            if (lesson != '\n') and (len(lesson.contents) > 1):
                                subject = lesson.contents[1].text.replace('\n', '').replace("                                                        ", '')
                                auditory = lesson.contents[3].text.replace('\n', '').replace("                                                        ", '')
                                teacher = lesson.contents[5].text.replace('\n', '').replace("                                                        ", '')
                                border = ''
                                if len(lesson.contents) == 9:
                                    border = lesson.contents[7].text.replace('\n', '').replace("                                                        ", '')
                                days[i] += (subject + '\n' + auditory + '\n' + teacher + '\n' + border + '\n' )
                                print(subject)
                                print(auditory)
                                print(teacher)
                                print(border)
                            pass
                i += 1
            except Exception as e:
                days[i] = "Пар нет. Кути, бухай, еби гусей!\n\n"
                pass
            pass
        else:
            break
    pass

print(os.getpid())
token = open("./token.token", 'r').readline()
bot = knocker.Knocker(token = token)
# main()
Farseer.SpawnConfig("SheduleBot")
while True:
    days = ["",""]
    sheduleSent = False
    hour = datetime.datetime.now().hour
    config = json.load(open('./config.json', 'r'))
    if hour == 6 and not sheduleSent:
        for group in config["Groups"]:
            main(group['url'])
            for peer in group['peers']:
                bot.SendMsg(messageText = days[0], peerId = peer)
        sheduleSent = True
    elif hour == 18 and not sheduleSent:
        for group in config["Groups"]:
            main(group['url'])
            for peer in group['peers']: 
                bot.SendMsg(messageText = days[1], peerId = peer)
        sheduleSent = True
    else:
        sheduleSent = False

    time.sleep(60)
