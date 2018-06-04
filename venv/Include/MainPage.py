from Download import request
from MongoQueue import MongoQueue
from bs4 import BeautifulSoup

spider_queue = MongoQueue('meinvxiezhenji', 'crawl_queue')
def start(url):
    print('enter start')
    response = request.get(url, 3)
    Soup = BeautifulSoup(response.text, 'lxml')
    all_a = Soup.find('div', class_='all').find_all('a')
    for a in all_a:
        title = a.get_text()
        url = a['href']
        print(url)
        spider_queue.push(url, title) ##将URL写入MongoDB的队列
if __name__ == "__main__":
    start('http://www.mzitu.com/all')