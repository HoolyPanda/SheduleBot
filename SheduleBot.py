import knocker
import vk_api
from bs4 import BeautifulSoup
# import curl
import requests
import datetime
import time
import os

days = ['','']
def main():
    url = "http://time-rtu.ru/?group=%D0%91%D0%91%D0%91%D0%9E-05-18"
    headers = {'accept': "*/*", "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0", "referer": "http://time-rtu.ru/?group=%D0%91%D0%91%D0%91%D0%9E-05-18"}

    session = requests.Session()
    b = session.get(url=url, headers=headers)
    a = BeautifulSoup(b.content, "html.parser")
    i = 0
    for card in a.find_all('div', attrs={"id":"card"}):
        if i < 2:
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
                            aaad = len(lesson.contents)
                            border = ''
                            if aaad == 9:
                                border = lesson.contents[7].text.replace('\n', '').replace("                                                        ", '')
                            days[i] += (subject + '\n' + auditory + '\n' + teacher + '\n' + border + '\n' )
                            print(subject)
                            print(auditory)
                            print(teacher)
                            print(border)
                        pass
            i += 1
            pass
        else:
            break
    pass

print(os.getpid())
nn = open("./token.token", 'r').readline()
bot = knocker.Knocker(token = nn)
main()
while True:
    vvv = datetime.datetime.now().hour
    if vvv == 7:
        bot.SendMsg(messageText = days[0], peerId = 160500068)
        time.sleep(3600)
    elif vvv == 18:
        bot.SendMsg(messageText = days[1], peerId = 160500068)
        quit()
    else:
        time.sleep(3600)

