#coding:utf8

import requests
import random
from lxml import etree
import time
import pandas as pd
from fake_useragent import UserAgent

class lianjiaSpider(object):
    def __init__(self, url):
        self.url = url
        self.blog = 1
        
    def get_header(self):
        ua = UserAgent()
        headers = {'User-Agent' : ua.chrome}
        return headers
    
    def get_html(self, url):
        if self.blog <= 3:
            try:
                res = requests.get(url = url, headers = self.get_header(), timeout = 3)
                html = res.text
                return html
            
            except Exception as e:
                print(e)
                self.blog += 1
                self.get_html(url)
                
    def parse_html(self, url):
        html = self.get_html(url)
        if html:
            p = etree.HTML(html)
            h_list = p.xpath('//ul[@class="sellListContent"]/li[@class="clear LOGVIEWDATA LOGCLICKDATA"]')
            data = {'name':[], 'infomation':[], 'unitprice':[]}
            for h in h_list:               
                name_list = h.xpath('.//a[@data-el="region"]/text()')
                if name_list:
                    data['name'].append(name_list[0])
                infomation_list = h.xpath('.//div[@class="houseInfo"]/text()')
                if infomation_list:
                    data['infomation'].append(infomation_list[0])
                else:
                   print('information error')
                
                price_list = h.xpath('.//div[@class="unitPrice"]/span/text()')
                if price_list:
                    data['unitprice'].append(price_list[0])
                else:
                    print('unitPrice error')
            #print(data)        
            info_website = pd.DataFrame(data)
            writer  = pd.ExcelWriter('lianjia.xlsx')
            info_website.to_excel(writer)
            writer.save()
            
    def run(self):
        try:
            url = self.url.format(1)
            self.parse_html(url)
            time.sleep(random.randint(1,3))
            self.blog = 1
        
        except Exception as e:
            print(e)
            
            
if __name__ == '__main__':
   spider = lianjiaSpider('https://bj.lianjia.com/ershoufang/pg{}/')
   spider.run()
   