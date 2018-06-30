import re
import requests
from bs4 import BeautifulSoup

#百度贴吧爬虫
class Spider(object):
    def __init__(self, baseUrl, seeLZ, floorFlag):
        """
        初始化
        :param baseUrl: 基地址
        :param seeLZ: 是否只看楼主
        :param floorFlag: 楼分隔符
        """
        self.baseUrl = baseUrl
        self.seeLZ = '?see_LZ=' + str(seeLZ)
        self.tool = Tool()
        self.file = None
        self.floor = 1
        self.defaultTitle = u'百度贴吧'
        self.floorFlag = floorFlag

    def getPage(self, pageIndex):
        """
        获取页面内容
        :param pageIndex: 页码
        :return: 页面内容
        """
        try:
            url = self.baseUrl + self.seeLZ + '&pn=' + str(pageIndex)
            response = requests.get(url)
            #print(response.content)
            return response.content.decode('utf-8')
        except BaseException as e:
            print(type(e))

    def getTitle(self, page):
        """
        获取帖子标题
        :param page: 页面内容
        :return: 帖子标题
        """
        #page = self.getPage(1)
        pattern = re.compile('<h1 class="core_title_txt.*?>(.*?)</h1>',re.S)
        title = re.search(pattern, page)
        if title:
            return title.group(1).strip()
        else:
            return None

    def getPageNum(self, page):
        """
        获取帖子页数
        :param page: 页面内容
        :return: 帖子页数
        """
        #page = self.getPage(1)
        pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
        pageNum = re.search(pattern, page)
        if pageNum:
            return pageNum.group(1).strip()
        else:
            return None

    def getContent(self, page):
        """
        获取每一层楼的内容
        :param page: 页面内容
        :return: 每一层楼的内容
        """
        try:
            pattern = re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
            #print("Get Content:", page)
            items = re.findall(pattern, page)
            contents = []
            #floor = 1
            if items:
                for item in items:
                    content = '\n' + self.tool.replace(item) + '\n'
                    contents.append(content)
                    #print(item)
                    #item = self.tool.replace(item)
                    #print(floor, u'楼------------------------------------------------------------------------------------------------------------------------------------\n')
                    #print(self.tool.replace(item))
                    #floor+=1
                return contents
            else:
                return None
        except TypeError as e:
            print(e.args)
        except BaseException as e:
            print(type(e))

    def setFileTitle(self, title):
        """
        设置文件标题
        :param title: 文件标题
        :return:
        """
        if title is not None:
            self.file = open(title + '.txt', 'w+')
        else:
            self.file = open(self.defaultTitle + '.txt', 'w+')

    def writeData(self, contents):
        """
        将数据写入文件
        :param contents: 文本内容
        :return:
        """
        try:
            for content in contents:
                if self.floorFlag == '1':
                    floorLine = '\n' + str(self.floor) + u'楼------------------------------------------------------------------------------------------------------------------------------------\n'
                    self.file.write(floorLine)
                print(content)
                self.file.write(content)
                self.floor += 1
        except TypeError as e:
            print("WriteData: ", e.args)
        except BaseException as e:
            print("WriteData: ", type(e))

    def start(self):
        """
        启动方法
        :return:
        """
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getTitle(indexPage)
        self.setFileTitle(title)

        if pageNum is None:
            print('URL已失效，请重试！')

        try:
            print('该帖子共有' + str(pageNum) + '页')
            for i in range(1, int(pageNum) + 1):
                print("正在写入第" + str(i) + "页数据")
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        except TypeError as e:
            print(e.args)
        except BaseException as e:
            print(type(e))
        finally:
            print("写入完成！")



# 处理页面标签类
class Tool(object):
    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        # strip()将前后多余内容删除
        return x.strip()

baseUrl = 'http://tieba.baidu.com/p/3138733512'
seeLZ = 0
floorTag = 1
spider = Spider(baseUrl,seeLZ, floorTag)
spider.start()
#page = spider.getPage(1).decode(encoding='utf-8')
#items = spider.getContent(page)


























