import requests
from bs4 import BeautifulSoup
import os
from Download import request
from pymongo import MongoClient
import datetime

class mzitu(object):
    def __init__(self):
        client = MongoClient()##与MongoDB建立连接，默认连接本地MongoDB数据库
        db = client['meinvxiezhenji']##选择数据库
        self.meizitu_collection = db['meizitu']##在数据库中选择一个集合
        self.title = ''##用来保存页面主题
        self.url = ''##用来保存页面地址
        self.img_urls = [] ##初始化一个列表，用来保存图片地址
        #self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"}

    def all_url(self, url):
        ##html = self.request(url)##调用request函数把套图地址传进去会返回给我们一个response
        html = request.get(url,3)
        all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find_all('a')
        for a in all_a:
            title = a.get_text()
            self.title = title ##将主题保存到self.title中
            print(u'开始保存：', title)
            path = str(title).replace('?', '_')## ？在Windows系统是不能创建文件夹的所以要替换掉
            self.mkdir(path)##调用mkdir函数创建文件夹
            os.chdir("D:\mzitu\\" + path)
            href = a['href']
            self.url = href ##将页面地址保存到self.url中
            if self.meizitu_collection.find_one({'主题页面':href}):##判断这个主题已经在数据库中，则忽略
                print(u'此页面已经爬取过了。')
            else:
                self.html(href)##调用html函数把href参数传递过去
    def html(self, href):##处理套图地址获得图片的页面地址
        html = request.get(href, 3)
        ##html = self.request(href)
        ##self.headers['referer'] = href
        pagenavi = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi')
        if pagenavi is not None:
            max_span = pagenavi.find_all('span')[-2].get_text()
            page_num = 0 ##充当计数器，判断图片是否下载完毕
            for page in range(1, int(max_span) + 1):
                page_num = page_num + 1
                page_url = href + '/' + str(page)
                self.img(page_url, max_span, page_num)

    def img(self, page_url, max_span, page_num):##处理图片页面地址获得图片的实际地址
        ##img_html = self.request(page_url)
        img_html = request.get(page_url, 3)
        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
        self.img_urls.append(img_url) ##将图片地址添加到列表中
        if int(max_span) == page_num:##当max_span与page_num相等时，就是最后一张图片了
            self.save(img_url)
            post = { ##构造一个字典
                '标题': self.title,
                '主题页面' : self.url,
                '图片地址' : self.img_urls,
                '获取时间' : datetime.datetime.now()
            }
            self.meizitu_collection.save(post) ##将post中的内容写入数据库
            print(u'插入数据库成功')
        else:
            self.save(img_url)
    def save(self, img_url):#保存图片
        name = img_url[-9:-4]
        print(u'开始保存：', img_url)
        ##img = self.request(img_url)
        img = request.get(img_url, 3)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()
    def mkdir(self, path):#创建文件夹
        path = path.strip()
        isExists = os.path.exists(os.path.join('D:\mzitu',path))
        if not isExists:
            print(u'创建一个名为', path, u'的文件夹')
            os.makedirs(os.path.join('D:\mzitu', path))
            ##os.chdir(os.path.join('D:\mzitu', path))
            return True
        else:
            print(u'名为', path, u'的文件夹已经存在！')
            return False
    """
        def request(self, url):##获取网页的response 然后返回
        content = requests.get(url, headers=self.headers)
        return content
    """


Mzitu = mzitu()#实例化
Mzitu.all_url('http://www.mzitu.com/all')##启动爬虫