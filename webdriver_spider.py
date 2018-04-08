import unittest

import time
from lxml import etree
from selenium import webdriver
from bs4 import BeautifulSoup as bs

class Douyu(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.number = 0
        self.numpage = 0
        # self.count = 0

    #测试方法必须要有test字样开头
    def testDouyu(self):
        self.driver.get('https://www.douyu.com/directory/all')
        while True:
            html = etree.HTML(self.driver.page_source)
            # soup = bs(self.driver.page_source,'lxml')
            #主播名
            content = html.xpath("//div[@class='mes']//p//span[@class='dy-name ellipsis fl']/text()")
            # content=soup.find_all('span',{'class':'dy-name ellipsis fl'})
            #房间名
            title = html.xpath("//div[@class='mes-tit']//h3[@class='ellipsis']/text()")
            # title = soup.find_all('h3',{'class':'ellipsis'})
            #关注人数
            numb =html.xpath("//div[@class='mes']//p//span[@class='dy-num fr']/text()")
            # numb = soup.find_all('span',{'class':'dy-num fr'})
            self.numpage +=1


            for contents,titles,nums in zip(content,title,numb):
                print(u'主播名：'+contents.strip()+u'\t房间名：'+titles.strip()+u'\t关注人数：'+nums.strip())
                self.number+=1
                # self.count+=int(nums.strip())
            print('第几页：', self.numpage)
            if self.driver.page_source.find('shark-pager-next shark-pager-disable shark-pager-disable-next')!=-1:
                break
            self.driver.find_element_by_class_name('shark-pager-next').click()
            time.sleep(3)
    #测试结束执行方式
    def tearDown(self):
        print('当前网站直播人数：'+str(self.number))

        self.driver.close()

if __name__ =="__main__":
    #启动测试模块
    unittest.main()