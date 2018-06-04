import requests
import re
import random
import time

class download(object):
    def __init__(self):
        self.iplist = []  ##初始化一个list用来存放获取到的IP
        html = requests.get("http://haoip.cc/tiqu.htm")
        iplistn = re.findall(r'r/>(.*?)<b', html.text, re.S)  ##表示从html.text中获取所有r/><b中的内容，re.S的意思是包括匹配包括换行符，findall返回的是个list
        for ip in iplistn:
            i = re.sub('\n', '', ip)  ##re.sub 是re模块替换的方法，这儿表示将\n替换为空
            self.iplist.append(i.strip())  ##添加到上面初始化的list里面, i.strip()的意思是去掉字符串的空格

        self.usr_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
    def get(self, url, timeout, proxy=None, num_retries=6):
        print(u'开始获取：', url)
        UA = random.choice(self.usr_agent_list) ##从self.user_agent_list中随机取出一个字符串
        headers = {'User-Agent':UA}##构造成一个完整的User-Agent （UA代表的是上面随机取出来的字符串)

        if proxy == None:##当代理为空时，不使用代理获取response
            try:
                response = requests.get(url, headers=headers, timeout=timeout)
                if response.status_code == 200:
                    return response
                else:
                    IP =''.join(str(random.choice(self.iplist)).strip())
                    proxy = {'http':IP}
                    return self.get(url, timeout, proxy)
            except:
                if num_retries > 0:##限定重试次数
                    time.sleep(10)##延迟10秒
                    print(u'获取网页出错，10S后将获取倒数第：', num_retries, u'次')
                    return self.get(url, timeout, num_retries-1)##调用自身并将次数减1
                else:
                    print(u'开始使用代理')
                    time.sleep(10)
                    IP = ''.join(str(random.choice(self.iplist)).strip())
                    proxy = {'http': IP}
                    return self.get(url, timeout, proxy, )
        else:
            try:
                IP = ''.join(str(random.choice(self.iplist)).strip())
                proxy = {'http': IP}
                response = requests.get(url, headers=headers, proxies=proxy, timeout=timeout)
                if response.status_code == 200:
                    return response
                else:
                    if num_retries > 0:  ##限定重试次数
                        time.sleep(10)  ##延迟10秒
                        IP = ''.join(str(random.choice(self.iplist)).strip())
                        proxy = {'http': IP}
                        print(u'正在更换代理，10S后将重新获取倒数第', num_retries, u'次')
                        print(u'当前代理是：', proxy)
                        return self.get(url, timeout, proxy, num_retries - 1)  ##调用自身并将次数减1
                    else:
                        print(u'代理失效！取消代理')
                        return self.get(url, 3)
            except:
                if num_retries>0:
                    time.sleep(10)
                    IP = ''.join(str(random.choice(self.iplist)).strip())
                    proxy = {'http':IP}
                    print(u'正在更换代理，10S后将重新获取倒数第', num_retries, u'次')
                    print(u'当前代理是：', proxy)
                    return self.get(url, timeout, proxy, num_retries - 1)
                else:
                    print(u'代理失效，取消代理！')
                    return self.get(url, 3)

request = download()


