import os
import knocker
import time

class Farseer:
    def __init__(self):
        while True:
            for file in os.listdir("./pidDir"):
                pid = open("./pidDir/" + file, 'r').readline().replace('\n', '')
                path = '/proc/' + pid
                if os.path.exists(path):
                    print("Pid ", file, ' is OK')
                else:
                    buddy = knocker.Knocker(token = open('./token', 'r').readline().replace('n',''))
                    buddy.SendMsg("PID: " + (file + ' - ' + pid) + " is not OK", peerId = 160500068)
            time.sleep(3600)
def SpawnConfig(name: str):
    userName = os.getlogin()
    if userName != 'root':
        config = open(str('/home/' + str(userName) + "/Farseer/pidDir/" + name), "w+")
    else:
        config = open(str('/' + str(userName) + "/Farseer/pidDir/" + name), "w+")
    config.write(str(os.getpid()))
    config.close()
    pass