import os
import knocker
import time

class Farseer:
    def __init__(self):
        while True:
            for folder in os.listdir("./users"):
                for file in os.listdir("./users/" + folder):
                    pid = open("./users/" + folder + "/" + file, 'r').readline().replace('\n', '')
                    path = '/proc/' + pid
                    if os.path.exists(path):
                        print("Pid ", file, ' is OK')
                    else:
                        buddy = knocker.Knocker(token = open('./token.token', 'r').readline().replace('n',''))
                        buddy.SendMsg("PID: " + (file + ' - ' + pid) + " is not OK", peerId = int(folder))
            time.sleep(120)
def SpawnConfig(name: str, peerId: int):
    userName = os.getlogin()
    if userName != 'root':
        try:
            os.mkdir("/home/" + str(userName) + "/Farseer/" + str(peerId))
        except Exception as e:
            print(str(e))
        config = open(str('/home/' + str(userName) + "/Farseer/" + str(peerId) + "/" + name), "w+")
    else:
        try:
            os.mkdir("/root" + "/Farseer/" + "users/" + str(peerId))
        except Exception as e:
            print(str(e))
        config = open(str('/' + str(userName) + "/Farseer/" + str(peerId) + "/" + name), "w+")
    config.write(str(os.getpid()))
    config.close()
    pass