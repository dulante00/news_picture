#!/usr/lib/env python
#_*_coding:utf-8_*_
'''
from urllib import urlopen
html=urlopen("http://news.boxun.com")
print html.read()

try:
    html=requests.get("http://www.google.com",headers={'Connection':'close'})
except ConnectionError:
    time.sleep(1)
    response = requests.get("http://www.google.com",headers={'Connection':'close'})
print(html.text)
'''
import requests
import re

#requests.adapters.DEFAULT_RETRIES = 5
#proxies = {'http': 'http://127.0.0.1:8087','https': 'http://127.0.0.1:8087'}

#img_data = requests.get(img_url,proxies=proxies )
#res = requests.get('http://news.boxun.com/news/gb/yuanqing/2016/04/201604251121.shtml',proxies=proxies)
#s = requests.session()
#s.keep_alive = False
#print(res.text)
src=' <ahref="javascript:;"class="dw_weibo">微博<ahref="java'
src=re.findall(r'[\u4e00-\u9fa5]',src)
#src=re.findall(r'http[\S]*?jpg',src)
print(len(src))