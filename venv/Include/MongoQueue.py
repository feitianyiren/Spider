from datetime import datetime, timedelta
from pymongo import MongoClient, errors

class MongoQueue(object):
    OUTSTANDING = 1##初始状态
    PROCESSING = 2 ## 正在下载状态
    COMPLETE = 3 ##下载完成状态

    def __init__(self, db, collection, timeout=300):##初始化MongoDB连接
        self.client = MongoClient()
        self.Client = self.client[db]
        self.db = self.Client[collection]
        self.timeout = timeout

    def __bool__(self):
        record = self.db.find_one(
            {'status':{'$ne':self.COMPLETE}}
        )
        return True if record else False
    def push(self, url, title):## 用来添加新加的URL进队列
        try:
            self.db.insert({'_id': url, 'status': self.OUTSTANDING, '主题': title})
            print(url, '插入队列成功')
        except errors.DuplicateKeyError as e:##报错代表已经在队列中了
            print(url,'已经存在于队列中了')
            pass
    def push_imgurl(self, title, url):
        try:
            self.db.insert({'_id': title, 'status': self.OUTSTANDING, 'url': url})
            print('图片地址插入成功')
        except errors.DuplicateKeyError as e:
            print('地址已经存在')
            pass
    def pop(self):
        """
        这个函数会查询队列中的所有状态为OUTSTANDING 的值，并更改状态，
        query为查询，update为更新并返回_id， 如果没有OUTSTANDING的值,
        则调用repair（）函数重置所有超时状态为OUTSTANDING
        """
        record = self.db.find_and_modify(
            query={'status': self.OUTSTANDING},
            update={'$set':{'status': self.PROCESSING, 'timestamp': datetime.now()}}
        )
        if record:
            return record['_id']
        else:
            self.repair()
            raise KeyError
    def pop_title(self, url):
        record = self.db.find_one({'_id':url})
        return record['主题']
    def peek(self):##这个函数是取出状态为OUTSTANDING的文档并返回_id
        record = self.db.find_one({'status': self.OUTSTANDING})
        if record:
            return record['_id']
    def complete(self,url):## 更新已完成的URL
        self.db.update({'_id': url}, {'$set': {'status': self.COMPLETE}})
    def repair(self):## 重置状态
        record = self.db.find_and_modify(
            query={
                'timestamp': {'$lt': datetime.now() - timedelta(seconds=self.timeout)},
                'status': {'$ne': self.COMPLETE}
            },
            update={'$set':{'status':self.OUTSTANDING}}
        )
        if record:
            print(u'重置URL状态', record['_id'])
    def clear(self):## 清除数据库，只有第一次调用，后续不要用，
        self.db.drop()















































