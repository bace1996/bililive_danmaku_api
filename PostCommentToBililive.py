import requests
import ast


class SendLiveDanmaku:
    precookie = ""
    roomid = ""
    message = ""
    fontsize = ""
    cookie = {}
    danmaku = {}
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.30 Safari/537.36',
    }
    url = "http://live.bilibili.com/msg/send"
    
    def __init__(self, cookie, roomid, message, fontsize):
        self.precookie = cookie;
        self.roomid = roomid;
        self.message = message;
        self.fontsize = fontsize;
        print("Initializing...");
        
    def parseCookie(self):
        data = self.precookie.split(";",21)
        cok = ""
        for x in range(0,len(data)-1):
            spa = data[x].split("=",2)
            cok += "'" + spa[0].lstrip(" ") + "': '" + spa[1] + "',\n"
        cok = "{" + cok + "}"
        self.cookie = ast.literal_eval(cok)
        
    def genDanmaku(self):
        danmaku = "{'color': '16777215','fontsize': '" + self.fontsize + "','mode': '1','msg': '" + self.message + "','rnd': '1454325444','roomid': '" + self.roomid + "',}"
        self.danmaku = ast.literal_eval(danmaku)
        
    def sendDanmaku(self):
        self.parseCookie()
        self.genDanmaku()
        r = requests.post(self.url, data=self.danmaku, headers=self.header, cookies=self.cookie)
        return r.text

mycookie = ""
msg = SendLiveDanmaku(mycookie, "157901", "nyaa", "25")
print msg.sendDanmaku()
print msg.danmaku
print msg.cookie

