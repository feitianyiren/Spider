import requests
from bs4 import BeautifulSoup
import re
import threading
import time

#糗事百科爬虫类
class Spider(object):

    #初始化方法
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = { 'User-Agent' : self.user_agent}
        #存放段子
        self.stories = []
        #是否继续运行
        self.enable  = False

    #传入页码获取页面
    def getPage(self, pageIndex):
        try:
            #构建URL
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            #获取网页内容
            response = requests.get(url, headers=self.headers)
            #将网页转化为UTF-8编码
            content = response.content.decode('utf-8')
            return content
        except NameError as e:
            print(e.args)
        except AttributeError as e:
            print(e.args)
        except BaseException as e:
            print(type(e))

    #传入页码，获取不带图片的段子列表
    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print("页面加载失败......")
            return None

        try:
            pattern = re.compile(
                '<div class="author clearfix">.*?<h2>(.*?)</h2>.*?<div.*?span>(.*?)</span>.*?<div class="stats">.*?"number">(.*?)</i>',
                re.S)
            items = re.findall(pattern, pageCode)
            #存储段子
            pageStories = []

            #遍历正则表达式匹配的信息
            for item in items:
                replaceBR = re.compile('<br/>')
                text = re.sub(replaceBR, '\n', item[1])
                # item[0]是一个段子的发布者，item[1]是内容，item[2]是点赞数
                pageStories.append([item[0].strip(), text.strip(), item[2].strip()])
        except IndexError as e:
            print(e.args)
            return None
        except NameError as e:
            print(e.args)
            return None
        except BaseException as e:
            print(type(e))
            return None

        return pageStories

    #加载并提取页面的内容，加入到列表
    def loadPage(self):
        #如果当前未看的页数少于2，则加载新一页
        if self.enable:
            if len(self.stories) < 2:
                #获取新一页
                pageStories = self.getPageItems(self.pageIndex)
                #将该页的段子存放到全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    #获取完之后页码索引加1
                    self.pageIndex += 1

    #调用该方法，每次敲回车打印输出一个段子
    def getOneStory(self, pageStories, page):
        for story in pageStories:
            #等待用户输入
            getInput = input()
            #每当输入回车一次，判断是否要加载新页面
            self.loadPage()
            #如果输入Q则程序结束
            if getInput == "Q":
                self.enable = False
                return
            print(u"第%d页\t发布人:%s\t\t赞:%s\n%s" %(page,story[0],story[2],story[1]))

    #开始方法
    def start(self):
        print(u"正在读取糗事百科,按回车查看新段子，Q退出")
        # 使变量为True，程序可以正常运行
        self.enable = True
        # 先加载一页内容
        self.loadPage()
        # 局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                #从全局list中获取一页段子
                pageStories = self.stories[0]
                #当前页数加1
                nowPage += 1
                #将全局list中第一个元素删除
                del self.stories[0]
                #输出该页段子
                self.getOneStory(pageStories, nowPage)

spider = Spider()
spider.start()






















