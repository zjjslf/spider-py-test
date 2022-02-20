#coding:utf8
from selenium import webdriver
import time
import pymongo
import pandas as pd

class seleniumSpider(object):
    def __init__(self, url, word):
        self.url = url
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=self.options)
        self.item = {'name':[], 'price':[], 'shop':[], 'count':[]}
        self.word = word 
        self.i = 0
       
    def login(self):
        self.browser.find_element_by_xpath('//div[@id="shortcut"]/div[@class="w"]/ul[@class="fr"]/li/a[@class="link-login"]').click()
        time.sleep(2)
        self.browser.find_element_by_xpath('//div[@id="content"]/div[@class="login-wrap"]/div[@class="w"]/div[@class="login-form"]/div[@class="login-tab login-tab-r"]/a').click()
        time.sleep(2)
        uname = input("username:")
        upassword = input("password:")
        self.browser.find_element_by_xpath('//*[@id="loginname"]').send_keys(uname)
        self.browser.find_element_by_xpath('//*[@id="nloginpwd"]').send_keys(upassword)
        self.browser.find_element_by_xpath('//div[@class="login-btn"]/a').click()
        
    def get_html(self):
        self.browser.get(self.url)
        self.browser.find_element_by_xpath('//*[@id="key"]').send_keys(self.word)
        self.browser.find_element_by_xpath('//div[@class="form"]/button').click()
        
    def get_data(self):
        #执行js语句拉动进度条
        self.browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        
        #给页面元素加载时预留时间
        time.sleep(5)
        
        #xpath提取商品信息
        li_list = self.browser.find_elements_by_xpath('//*[@id="J_goodsList"]/ul/li')
        
        #遍历商品信息，提取并保存
        
        for li in li_list:
            self.item['name'].append(li.find_element_by_xpath('.//div[@class="p-name"]/a/em').text.strip())
            self.item['price'].append(li.find_element_by_xpath('.//div[@class="p-price"]/strong/i').text.strip())
            self.item['shop'].append(li.find_element_by_xpath('.//div[@class="p-shopnum"]').text.strip())
            self.item['count'].append(li.find_element_by_xpath('.//div[@class="p-commit"]/strong').text.strip())
            self.i += 1
           
        
        
    def run(self):
    
        countnum = 0
        
        #获取搜索结果
        self.get_html()
        
        #循环执行点击"下一页"操作
        while  True:
            #获取每一页的数据 
            self.get_data()
                    
            #判断是否是最后一页
            if self.browser.page_source.find('<b>100</b><em>/</em><i>100</i>') > 0:
                print(self.i)
                break    
            else:
                countnum += 1
                self.browser.find_element_by_class_name('fp-next').click()
                time.sleep(5)
                print(countnum)

        self.browser.quit()
        
        info_website = pd.DataFrame(self.item)
        writer  = pd.ExcelWriter('jd.xlsx')
        info_website.to_excel(writer)
        writer.save()

if __name__ == '__main__':
    spider = seleniumSpider('http://www.jd.com/', "python书籍")
    spider.run()