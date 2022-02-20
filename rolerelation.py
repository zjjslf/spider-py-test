import getpass
import requests
import re
import json
import time
import hashlib

import http.cookiejar, urllib.request
base_url = 'https://weibo.com/p/1006051195813710/follow?page=1'

def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }

    response = requests.get(url, headers = headers)
    if response.status_code == 200:
        return response.text
    else:
        print("error")
    return None

def role(url):
    html = get_one_page(url)
    print(html)
    #news_data = json.loads(html,encoding='utf-8')
    #for n in news_data['data']['pc_feed_focus']:
    #    print()
    #roleid = re.search('.*?$CONFIG[\'page_id\']=\'(.*?)\';.*?', html)
    #print(roleid)
        
        
if __name__ == '__main__':
    role(base_url)   

