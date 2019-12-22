import requests
from bs4 import BeautifulSoup
import re
import random
from fake_useragent import UserAgent
from analyze.db import Connect
from analyze.calculate import Calculate
from analyze.paint import Paint

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

def get_price(i,language):
    '''
    :parameter：i为页数，language为要爬取的招聘编程语言
    :return:result  以列表字典的形式输出，包含最低工资，最高工资，发放月份及工作城市
    '''
    result=[]
    proxies = {'http': 'http://%s' % (random_proxy())}
    headers={
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip,deflate,br',
        'Connection': 'Upgrade',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'User-Agent': Change_UA(),
        'referer':'https://www.liepin.com/zhaopin/?key=python&d_sfrom=search_industry'
    }
    context=requests.get(url='https://www.liepin.com/zhaopin/?init=-1&headckid=e4818fb94bd18c4a&fromSearchBtn=2&ckid=e4818fb94bd18c4a&degradeFlag=0&key='+str(language)+'&siTag=p_XzVCa5J0EfySMbVjghcw%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_prime&d_ckId=19b62f82bebd938c8f0a2fa964e3fcb3&d_curPage=0&d_pageSize=40&d_headId=19b62f82bebd938c8f0a2fa964e3fcb3&curPage='+str(i),
                         headers=headers,
                         proxies=proxies,timeout=5
                         )
    context=context.text
    soup=BeautifulSoup(context,'html.parser')
    prices=soup.find_all(attrs={'class':'text-warning'})
    areas=soup.find_all(attrs={'class':'area'})
    for i in range(0,len(prices)):
        if areas[i].string==None:
            print('areas[i] %s' %areas[i])
            continue
        min_price = re.search('(\d*)-', prices[i].string)
        max_price = re.search('-(\d*)k·', prices[i].string)
        mouth = re.search('·(\d*)薪', prices[i].string)
        area=re.search('(.*?)-',areas[i].string)

        if area==None:
            area=areas[i].string
        else:
            area=area.group(1)

        if min_price==None or max_price==None or mouth==None:
            pass
        else:
            result.append(
                {
                    "min_price": min_price.group(1),
                    "max_price": max_price.group(1),
                    "mouth": mouth.group(1),
                    "area": area,
                }
            )

    return result


def insert():
    '''
    爬取信息存储
    :return:
    '''
    conn = Connect()
    conn.conn()
    for i in range(100):
        try:
            result = get_price(i, 'python')
            conn.insert_python(result)
        except Exception:
            print('第 %s 页爬取失败' % i)

    for i in range(100):
        try:
            result = get_price(i, 'Java')
            conn.insert_Java(result)
        except Exception:
            print('第 %s 页爬取失败' % i)

    for i in range(100):
        try:
            result = get_price(i, 'PHP')
            conn.insert_PHP(result)
        except Exception:
            print('第 %s 页爬取失败' % i)

    print('爬取完成')



if __name__ == '__main__':
    # get_proxy()
    conn = Connect()
    conn.conn()
    calculate=Calculate(conn)
    avg=calculate.avg_sal()
    paint=Paint()
    paint.paint(avg)

    min_python=calculate.min_price('python')
    max_python=calculate.max_price('python')
    min_java=calculate.min_price('java')
    max_java=calculate.max_price('java')
    min_php=calculate.min_price('php')
    max_php=calculate.max_price('php')

    paint.index_paint(min_python,max_python,'Python')
    paint.index_paint(min_java,max_java,'Java')
    paint.index_paint(min_php,max_php,'PHP')
