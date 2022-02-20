
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
    pattern = re.compile('\{"rate":"(.*?)","cover_x".*?title":"(.*?)","url":"(.*?)","pl.*?,"is_new".*?\}', re.S)
    items = re.findall(pattern, html)

    for item in items:
        yield {
            'title':item[1],
            'href':item[2].replace("\\",""),
            'score':item[0],
        }


def write_to_file(content):
    with open('E:\\pytondata\\doubanmovie3.txt', 'a', encoding = 'utf-8') as f:
        f.write(json.dumps(content, ensure_ascii = False) + '\n')

def main(offset):
    url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%BB%8F%E5%85%B8&sort=rank&page_limit=20&page_start=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)

if __name__ == '__main__':
    j = 0
    for i in range(50):
        main(offset = i * 20)
        j = j + 1
        print(j)
        

