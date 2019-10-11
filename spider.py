#!/usr/bin/env python
# -*- coding:utf-8 -*-
# datetime:19-8-29 下午8:02
# project: spider


import queue as Queue
import requests
import re, os, sys, random
import threading
import logging
import time
from requests.exceptions import ConnectTimeout,ConnectionError
from tools import GetItem


proxies = {"http": "socks5://127.0.0.1:1080",
           "https": "socks5://127.0.0.1:1080"}   # 科学上网

# 日志模块
logger = logging.getLogger("AppName")
formatter = logging.Formatter('%(asctime)s %(levelname)-5s: %(message)s')
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

q = Queue.Queue()       #url队列
page_q = Queue.Queue()  # 页面
getItem = GetItem()


def download():
    global q
    while True:
        vurl = q.get()
        if vurl is None:
            break
        video_id = vurl.split('=')[-1]

        if getItem.already_download(video_id):
            print('%s has already existed in downloads folder,skip it .' % video_id)

        logger.info(u"*Downloading：%s" % video_id)
        try:
            getItem.download(vurl)
        except Exception as e:
            print(e, '#some thing wrong in :#', video_id)
            q.task_done()
            continue
        logger.info(u"down load completed:：%s" % video_id)
        q.task_done()
        time.sleep(random.randint(3,10))


def get_page(keyword):
    global page_q
    while True:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        page = page_q.get()
        if page is None:
            break
        # url = "https://www.youtube.com/results?sp=EgIIAg%253D%253D&search_query=" + keyword + "&page=" + str(page)
        url = "https://www.youtube.com/results?search_query=" + keyword + "&page=" + str(page)
        try:
            html = requests.get(url, headers=headers, proxies=proxies).text
        except (ConnectTimeout,ConnectionError):
            print(u"访问超时,可能没有科学上网~_~!")
            os._exit(0)  # 用于线程推出,直接推出python interpreter
                         #  sys.exit()  # 用于主线程推出，raise 一个SystemExit异常
        reg = re.compile(r'"url":"/watch\?v=(.*?)","webPageType"', re.S)    # re.S点任意匹配模式
        results = reg.findall(html)
        results_dedup = set([x.split('\\')[0] for x in results])
        logger.info(u"第 %s 页" % page)
        for v_id in results_dedup:
            vurl = "https://www.youtube.com/watch?v=" + v_id
            q.put(vurl)
        page_q.task_done()
        time.sleep(1)
 
def run():
    # 使用帮助
    keyword = input(u"请输入关键字： ")
    threads = int(input(u"请输入线程数量(建议1-10): "))
    page_num = int(input(u'请输入爬取的页面数量: '))
    # 判断目录
    path = os.path.join(os.getcwd(),'downloads')
    if not os.path.exists(path):
        os.makedirs(path)
    # 解析网页
    logger.info(u"开始解析网页")
    for page in range(1,page_num+1):
        page_q.put(page)
    for y in range(threads):
        t = threading.Thread(target=get_page, args=(keyword,))
        t.setDaemon(True)
        t.start()
    page_q.join()
    logger.info(u"=========共 %s 个视频===========" % q.qsize())
    # 多线程下载
    logger.info(u"开始下载:")
    for x in range(threads):
        t = threading.Thread(target=download)
        t.setDaemon(True)
        t.start()
    q.join()
    logger.info(u"所有视频下载完成！")


if __name__ == '__main__':
    run()
