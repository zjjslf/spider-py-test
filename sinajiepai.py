
import requests
import re
import json
import time
from urllib.parse import urlencode
import os
from hashlib import md5


def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        }

    response = requests.get(url, headers = headers)
    if response.status_code == 200:
        return response.text
    return None


def save_image(item):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        }
    path = 'E:\\pytondata\\头条街拍\\' + item.get('title')
    if not os.path.exists(path):
        os.mkdir(path)

    try:
        response = requests.get(item.get('image'), headers = headers)
        if response.status_code == 200:
            imagepath = path + os.path.sep + '{file_name}.{file_suffix}'.format(
                file_name=md5(response.content).hexdigest(),
                file_suffix = 'jpg')
            if not os.path.exists(imagepath):
                with open(imagepath, 'wb') as f:
                    f.write(response.content)
            else :
                print("exist")
        else:
            print('image not exist')
    except requests.ConnectionError:
        print('Failed To Save Image')

def get_image(json):
    if json.get('data'):
        for item in json.get('data'):
            title = str(item.get('title')).replace(":", "").replace("?", "")
            images = item.get('image_list')
            if images:
                for image in images:
                    imageurl = image.get('url').replace("list", "large").replace("190x124/", "")
                    print(title+":"+imageurl)
                    yield {
                        'image': imageurl,
                        'title': title
                    }
            else:
                print('image is none')
    else:
        print('data is none')

def main(offset):
    params = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20'
    }

    #基础地址
    base_url = 'https://www.toutiao.com/api/search/content/?'
    url = base_url + urlencode(params)
    html = get_one_page(url)
    data = json.loads(html)
    for item in get_image(data):
        save_image(item)

if __name__ == '__main__':
    for i in range(2,10):
        main(offset = i * 20)
        

