import requests
from bs4 import BeautifulSoup
import os
from Download import request
from pymongo import MongoClient

class mzitu(object):
    """
        def __init__(self):
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"}
    """

    def all_url(self, url):
        ##html = self.request(url)##调用request函数把套图地址传进去会返回给我们一个response
        html = request.get(url,3)
        all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find_all('a')
        for a in all_a:
            title = a.get_text()
            print(u'开始保存：', title)
            path = str(title).replace('?', '_')## ？在Windows系统是不能创建文件夹的所以要替换掉
            self.mkdir(path)##调用mkdir函数创建文件夹
            os.chdir("D:\mzitu\\" + path)
            href = a['href']
            self.html(href)##调用html函数把href参数传递过去
    def html(self, href):##处理套图地址获得图片的页面地址
        html = request.get(href, 3)

        ##html = self.request(href)
        ##self.headers['referer'] = href
        pagenavi = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi')
        if pagenavi is not None:
            max_span = pagenavi.find_all('span')[-2].get_text()
            for page in range(1, int(max_span) + 1):
                page_url = href + '/' + str(page)
                self.img(page_url)

    def img(self, page_url):##处理图片页面地址获得图片的实际地址
        ##img_html = self.request(page_url)
        img_html = request.get(page_url, 3)
        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
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