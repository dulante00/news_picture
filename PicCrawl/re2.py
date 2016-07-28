# -*- coding:utf-8 -*-  
'''import urllib
url = 'http://i.epochtimes.com/assets/uploads/2016/07/IMG_5515-600x400.jpg'
name ='/Users/cp3/Desktop/2.jpg'
#保存文件时候注意类型要匹配，如要保存的图片为jpg，则打开的文件的名称必须是jpg格式，否则会产生无效图片  
proxies = {'http': 'http://127.0.0.1:8087', 'https': 'http://127.0.0.1:8087'}
conn = urllib.urlopen(url,proxies)
f = open(name,'wb')  
f.write(conn.read())  
f.close()  
print 'Pic Saved!'
'''
#下载网页中的图片到本地
import urllib.request
handler=urllib.request.ProxyHandler({'http': 'http://127.0.0.1:8087', 'https': 'http://127.0.0.1:8087'})
opener=urllib.request.build_opener(handler)
response=opener.open('http://i.epochtimes.com/assets/uploads/2016/07/IMG_5515-600x400.jpg')
name ='/Users/cp3/Desktop/2.jpg'
f=open(name,'wb')
f.write(response.read())
f.close()
print('Pic Saved!')