import requests
#导入进程池模块
from multiprocessing import Pool
from requests.exceptions import RequestException
import re
import json

headers = {
'Host': 'maoyan.com',
'Connection': 'keep-alive',
'Cache-Control': 'max-age=0',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Referer': 'https://maoyan.com/films',
'Accept-Language': 'zh-CN,zh;q=0.9',
}


def get_one_page(url,headers,verify):
    try:
        sess = requests.session()

        # sess = requests.session()
        response = sess.get(url=url,headers=headers,verify=verify)

        #判断是否请求成功

        if response.status_code == 200:
            #若请求成功则返回，页面信息
            return response.text
        return None
    except:
        return None

#解析获取的网页
def parse_one_page(html):
    pattern = re.compile(r'<dd>.*?movie-poster">.*?data-src="(.*?)".*?}">(.*?)</a>.*?integer">(.*?)</i>.*?fraction">(\d+)</i>',re.S)
    items = re.findall(pattern,html)
    # print(items)
    for item in items:
        yield {
        'title':item[1],
        'image':item[0],
        'score':item[2]+item[3]
        }
#将数据写入文件
def write_to_file(content):
    #设置json数据显示中文
    with open('result.txt','a',encoding='utf-8') as f:
        #ensure_ascii=False 表示上传的json数据，不按照ascii码
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()

#获取响应信息
def main(offset):
    url = 'https://maoyan.com/films?showType=3&offset='+str(offset)
    # headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}

    #调用请求
    html = get_one_page(url=url,headers=headers,verify=False)
    # print(html)
    for itme in parse_one_page(html):
        print(itme)
        write_to_file(itme)
if __name__ == '__main__':
    # for i in range(10):
    #     main(i*30)
    #创建进程池对象
    pool = Pool()
    pool.map(main,[i*10 for i in range(100)])


