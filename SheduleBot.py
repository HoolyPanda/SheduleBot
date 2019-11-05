import knocker
import vk_api
from bs4 import BeautifulSoup
import requests
import datetime
import time
import os
import Farseer
import json


days = ['', '']

class SheduleBot:
    def __init__(self):
        self.group = None
        pass
    def main(self, targetUrl: str):
        if targetUrl == "":
            url = "http://time-rtu.ru/?group=%D0%91%D0%91%D0%91%D0%9E-05-18"
        else:
            url = targetUrl
        headers = {'accept': "*/*",
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0",
                "referer": url}

        session = requests.Session()
        rawHtml = session.get(url=url, headers=headers)
        preParsedHtml = BeautifulSoup(rawHtml.content, "html.parser")
        i = 0
        for card in preParsedHtml.find_all('div', attrs={"id": "card"}):
            if i < 2:
                try:
                    if days[i] == "":
                        date = card.contents[1].text.replace(
                            "\n", '').replace(" ", '')
                        days[i] += (date + "\n")
                        print(date)
                        for _lesson in card.contents[3].contents[1]:
                            if _lesson != "\n" and _lesson != 'Выходной':
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
                                        days[i] += (subject + '\n' + auditory +
                                                    '\n' + teacher + '\n' + border + '\n')
                                        print(subject)
                                        print(auditory)
                                        print(teacher)
                                        print(border)
                                        if subject == '- - - - - - - - - - - - - - - - - - - - - - - ':
                                            if self.group["finalClassEnds"] == "":
                                                self.group["finalClassEnds"] = time.replace(" ", "")
                                            else:
                                                pass

                                    pass
                            elif _lesson == 'Выходной':
                                if i == 1:
                                    days[i] = "Завтра пар нет. Кути, бухай, еби гусей!\n\n"
                                elif i == 0:
                                    days[i] = "Сегодня пар нет. Кути, бухай, еби гусей!\n\n"
                    i += 1
                except Exception as e:
                    print(str(e))
                    pass
                pass
            else:
                break
        pass


print(os.getpid())
token = open("./token.token", 'r').readline()
bot = knocker.Knocker(token=token)
Farseer.SpawnConfig(name = "SheduleBot", peerId = 160500068)
sheduleBot = SheduleBot() 
while True:
    days = ["", ""]
    currentTime = str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute)
    config = json.load(open('./config.json', 'r'))
    for group in config["Groups"]:
        sheduleBot.group = group
        if currentTime == "6:00":
            sheduleBot.main(targetUrl= group['url'])
            for peer in group['peers']:
                bot.SendMsg(messageText=days[0], peerId=peer)
            pass
        elif currentTime == group["finalClassEnds"]:
            sheduleBot.main(group['url'])
            for peer in group['peers']:
                bot.SendMsg(messageText=days[1], peerId=peer)
                pass
            group["finalClassEnds"] = ""
    json.dump(config, open("./config.json", "w"))
    time.sleep(30)
