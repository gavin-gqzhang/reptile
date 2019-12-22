import re
import requests
import threading
import time
import random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pymysql


def Change_UA():
    '''
    访问UA切换，引入fake_useragent包
    单次访问单次调用，保证每次UA切换
    共模拟浏览器：ie，chrome，firefox，safari
    :return: UA
    '''
    ua=UserAgent()
    browser=['ie','chrome','firefox','safari']
    return ua[(browser[random.randint(0,3)])]

def get_proxy():
    '''
    爬取快代理网站，爬取第一页代理，时间可保证在当天时间，后续页代理不可靠
    其他国内高匿代理网站：https://www.xicidaili.com/nn/
    :return: 代理列表
    '''
    global proxys
    proxys=[]
    content=requests.get("https://www.kuaidaili.com/free/inha/1/")
    content.encoding=content.apparent_encoding
    text=content.text
    soup=BeautifulSoup(text,'html.parser')
    soup=soup.tbody
    IPS=soup.find_all(attrs={'data-title':'IP'})
    PORTS=soup.find_all(attrs={'data-title':'PORT'})
    # print('%s:%s'% (IPS[0].string,PORTS[0].string))
    for i in range(0,len(IPS)):
        proxy='%s:%s' %(IPS[i].string,PORTS[i].string)
        proxys.append(proxy)

def random_proxy():
    '''
    将获取到的proxy进行随机化获取，每次调用该函数，代理不唯一
    :return:   proxy
    '''
    proxy=proxys[random.randint(0,len(proxys)-1)]
    return proxy

def conn_db(href):
    '''
    链接数据库，接受url参数，保存到数据库中
    :param href:
    :return: None
    '''
    conn=pymysql.connect(host='127.0.0.1',user='root',password='123456',db='github',charset='utf8')
    cursor=conn.cursor()
    try:
        insert = "insert into github.url(href) values ('%s');" %(href)
        cursor.execute(insert)
    except Exception as  e:
        print('%s 插入数据失败' %href)
    else:
        conn.commit()
        print('插入数据成功')
    cursor.close()
    conn.close()

def get(url,referer):
    proxies = {'http': 'http://%s' % (random_proxy())}
    global no_get
    UA=Change_UA()
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip,deflate,br',
        'Connection': 'Upgrade',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'User-Agent': UA,
        'referer': referer
    }
    try:
        content = requests.get(url=url, headers=headers, proxies=proxies, timeout=5)
        return content
    except requests.exceptions.RequestException as  e:
        print('无法访问：%s' %url)
        return None

# print(get('https://github.com',''))

def get_link(url):
    '''
    爬取所有压缩包链接，添加到数据库中
    :return: None
    '''
    links=[]
    '''
    proxies = {'http': 'http://%s' % (random_proxy())}
    UA=Change_UA()
    
    url='https://github.com/search?l=Python&p='+str(count)+'&q=python&type=Repositories'
    '''

    # print('第 %s 页' %count)
    '''
    headers={
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip,deflate,br',
        'Connection': 'Upgrade',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'User-Agent': UA,
        'referer': url
    }
    content=requests.get(url=url,headers=headers,proxies=proxies,timeout=10)
    '''
    referer='https://github.com'
    content=get(url=url,referer=referer)
    if content==None:
        return
    hrefs=re.findall(r'href="/[^/]+/[^"^/]+">',content.text)[1:]
    for i in hrefs:
        href='https://github.com'+re.findall(r'/[^/]+/[^"^/]+',i)[0]
        '''
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip,deflate',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'User-Agent': UA,
            'referer': href
        }
        zip_content=requests.get(href,headers=headers,proxies=proxies)
        '''
        zip_content=get(url=href,referer=url)
        if zip_content==None:
            return
        zip_hrefs=re.findall(r'href="[^"]+.zip"',zip_content.text)[0]
        zip_href='https://github.com'+re.findall(r'[^"]+.zip',zip_hrefs)[0]
        # links.append(zip_href)
        conn_db(zip_href)
    return
    # return links


'''
    第一种线程爬取方法，存在等待相应超时，导致其他线程进行
    定义变量count，建立五个线程，同时爬取网页数据，延时为2
    五个线程导致访问网站延时和时间延时，对于访问时间过长的网页直接跳过爬取


count=1
while count<=100:
    # print('第 %s 到 %s 页' % (count,count+4))
    tread1=threading.Thread(target=get_link,args=(count,)).start()
    time.sleep(10)
    tread2=threading.Thread(target=get_link,args=(count+1,)).start()
    time.sleep(10)
    tread3=threading.Thread(target=get_link,args=(count+2,)).start()
    time.sleep(10)
    tread4=threading.Thread(target=get_link,args=(count+3,)).start()
    time.sleep(10)
    tread5=threading.Thread(target=get_link,args=(count+4,)).start()
    time.sleep(10)

    count=count+5
'''

'''
class MyThread(threading.Thread):
    def __init__(self,function,args=()):
        super(MyThread,self).__init__()
        self.function=function
        self.args=args

    def run(self):
        self.result=self.function(*self.args)

    def get_result(self):
        return self.result

def main():
    pages=[]
    no_page=[]
    threads=[]
    get_proxy()
    count=1
    while  count<=100:
        thread1 = MyThread(get_link,args=(count,))
        threads.append(thread1)
        thread1.start()
        time.sleep(5)
        thread2 = MyThread(get_link, args=(count+1,))
        threads.append(thread2)
        thread2.start()
        time.sleep(5)
        thread3 = MyThread(get_link, args=(count+2,))
        threads.append(thread3)
        thread3.start()
        time.sleep(5)
        thread4 = MyThread(get_link, args=(count+3,))
        threads.append(thread4)
        thread4.start()
        time.sleep(5)
        thread5 = MyThread(get_link, args=(count+4,))
        threads.append(thread5)
        thread5.start()
        time.sleep(5)

        for thread in threads:
            thread.join()
            pages.append(thread.get_result())

        count=count+5

    for i in range(1,101):
        if i not in pages:
            no_page.append(i)

    print('未爬取完成的页面： %s' %no_page)

main()

'''

def select():
    '''
    获取到数据库中的全部链接，保存在result中
    :return:  result
    '''
    conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='github', charset='utf8')
    cursor = conn.cursor()
    try:
        sqlli="select href from github.url"
        cursor.execute(sqlli)
        result=cursor.fetchall()
    except Exception as  e:
        print('获取数据失败')
    cursor.close()
    conn.close()
    return result

def download(url,pk):
    '''
    下载函数
    :param url:
    :return:
    '''
    status=0
    proxies = {'http': 'http://%s' % (random_proxy())}
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip,deflate,br',
        'Connection': 'Upgrade',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'User-Agent': Change_UA(),
        'referer': get_referer(url=url)
    }
    try:
        print('开始访问 %s' %url)
        r = requests.get(url=url, headers=headers, proxies=proxies,timeout=10)
    except requests.RequestException as e:
        for i in range(3):
            try:
                r=requests.get(url=url, headers=headers, proxies=proxies,timeout=10)
                status=r.status_code
            except requests.RequestException as e:
                pass

            if status==200:
                break
        if status!=200:
            print('%s 无法下载' %url)
            return
    path = 'H:\GitHub\%s.zip' % pk
    with open(path, 'wb') as code:
        code.write(r.content)


def get_referer(url):
    '''
    根据url获取referer
    :param url:
    :return: referer
    '''
    referer = ''
    count = 0
    for i in url:
        if i == '/':
            count = count + 1
        if count == 5:
            break
        referer = referer + i
    return referer

def main():
    count=0
    get_proxy()
    download_url=select()
    for i in download_url:
        download(url=i[0],pk=count)
        count=count+1

if __name__ == '__main__':
    main()