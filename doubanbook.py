
import requests
import re
import json
import time


def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        }

    response = requests.get(url, headers = headers)
    if response.status_code == 200:
        return response.text
    return None

def parse_one_page(html):
    pattern = re.compile('<li class="subject-item".*?<a href="(.*?)" title="(.*?)".*?"pub">(.*?)</div>.*?nums">(.*?)</span>.*?"pl">(.*?)</span>', re.S)
    items = re.findall(pattern, html)

    for item in items:
        yield {
            'title':item[1],
  #          'href':item[0],
  #          'author':item[2].strip(),
  #          'score':item[3],
  #          'pl':item[4].strip().lstrip('(').rstrip(')')
        }


def write_to_file(content):
    with open('E:\\pytondata\\doubanread2.txt', 'a', encoding = 'utf-8') as f:
        f.write(json.dumps(content, ensure_ascii = False) + '\n')

def main(offset):
    url = 'https://book.douban.com/tag/%E5%8E%86%E5%8F%B2?start=' + str(offset) + '&type=S'
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)

if __name__ == '__main__':
    j = 0
    for i in range(50):
        main(offset = i * 20)
        j = j + 1
        print(j)
        

