import os
import time
import threading
import multiprocessing
from MongoQueue import MongoQueue
from Download import request
from bs4 import BeautifulSoup

SLEEP_TIME = 1

def mzitu_crawler(max_threads=10):
    crawl_queue = MongoQueue('meinvxiezhenji', 'crawl_queue')
    img_queue = MongoQueue('meinvxiezhenji', 'img_queue')
    def pageurl_crawler():
        while True:
            try:
                url = crawl_queue.pop()
                print(url)
            except KeyError:
                print('队列没有数据')
                break
            else:
                img_urls = []
                req = request.get(url, 3).text
                title = crawl_queue.pop_title(url)
                path = str(title).replace('?','')
                mkdir(path)
                os.chdir('D:\mzitu\\' + path)
                pagenavi = BeautifulSoup(req, 'lxml').find('div', class_='pagenavi')
                if pagenavi is not None:
                    max_span = pagenavi.find_all('span')[-2].get_text()
                    for page in range(1, int(max_span) + 1):
                        page_url = url + '/' + str(page)
                        img_url = BeautifulSoup(request.get(page_url, 3).text, 'lxml').find('div', class_='mian-iamge').find('img')['src']
                        print(img_url)
                        img_urls.append(img_url)
                        save(img_url)
                    crawl_queue.complete(url)##设置为完成状态
                    img_queue.push_imgurl(title, img_urls)
    def save(img_url):#保存图片
        name = img_url[-9:-4]
        print(u'开始保存：', img_url)
        ##img = self.request(img_url)
        img = request.get(img_url, 3)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()
    def mkdir(path):#创建文件夹
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

    threads = []
    while threads or crawl_queue:
        """
        crawl_queue用上__bool__函数的作用，为真则代表MongoDB队列里面还有数据
        threads 或者 crawl_queue为真都代表还没下载完成，程序就会继续执行
        """
        for thread in threads:
            if not thread.is_alive():##is_alive判断是否为空，不为空则在队列中删掉
                threads.remove(thread)
        while len(threads) < max_threads or crawl_queue.peek():
            thread = threading.Thread(target=pageurl_crawler)
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)
        time.sleep(SLEEP_TIME)
def process_crawler():
    process = []
    num_cpus = multiprocessing.cpu_count()
    print('将会启动进程数为：', num_cpus)
    for i in range(num_cpus):
        print('启动线程：', i)
        p = multiprocessing.Process(target=mzitu_crawler)
        p.start()
        process.append(p)
    for p in process:
        p.join()
if __name__ == '__main__':
    process_crawler()





















