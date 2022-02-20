#coding:utf8

import requests
import random
import time
from hashlib import md5
from fake_useragent import UserAgent

class YoudaoSpider(object):
    def __init__(self, url):
        self.url = url
        
    def get_header(self):
        ua = UserAgent()
        headers = {'User-Agent' : ua.chrome}
        return headers
    
    def get_lts_salt_sign(self, word):
        lts = str(int(time.time()*1000))
        salt = lts + str(random.randint(0,9))
        string = "fanyideskweb" + word + salt + "Y2FYu%TNSbMCxc3t2u^XT"
        s = md5()
        s.update(string.encode())
        sign = s.hexdigest()
        
        return lts, salt, sign
        
    def attack_yd(self, word):
        lts, salt, sign = self.get_lts_salt_sign(word)

        data = {
                "i" :word,
                "from":"AUTO" ,              
                "to": "AUTO",
                "smartresult":"dict",
                "client": "fanyideskweb",
                "salt": salt,
                "sign": sign,
                "lts": lts,
                "bv": "56d33e2aec4ec073ebedbf996d0cba4f",
                "doctype": "json",
                "version": "2.1",
                "keyfrom": "fanyi.web",
                "action": "FY_BY_REALTlME"
        }
        
        res = requests.post(url = self.url, data = data, headers = self.get_header())
        html = res.json()
        result = html["translateResult"][0][0]["tgt"]
        print(result)
        
    def run(self):
        try:
            word = input("parse:")
            print(word)
            self.attack_yd(word)
        
        except Exception as e:
            print(e)
            
            
if __name__ == '__main__':
   spider = YoudaoSpider('http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule')
   spider.run()
   