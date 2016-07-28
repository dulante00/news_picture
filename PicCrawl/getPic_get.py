#!/usr/bin/env python
#_*_coding:utf-8_*_
import shutil
import urllib.request
import re
from urllib.error import HTTPError
from PIL import Image
import os
import requests
TIMEOUT=50
MIN_PIC_SIZE=20000
MAX_PIC_COUNT=8
PIC_BEGIN=1
dest_path_count=0  #记录所有正文图片个数
#targetDir = r"/Users/cp3/Desktop/pic"
#count指代要删除到的图片的标记数
def picDelete(filename,count):
    path=filename
    for i in range(PIC_BEGIN,count):
        filename=path.format(i)  #图片的具体路径
        if os.path.exists(filename):  # 检查指定文件是否存在
            os.remove(filename)  # 存在则删除
            #print("删除成功!")
        else:
            print("文件不存在!")
#将多余的图片删除(删除到计数count_pic)
def picCount(path,pic_count):
    dic = {}
    list = []
    for i in range(PIC_BEGIN, pic_count + 1):
        image1 = Image.open(path.format(i))
        dic[i] = picSize(image1)
    #print(dic)
    for i in range(PIC_BEGIN, pic_count):
        x, y = dic[i]
        # print(x,y)
        a, b = dic[i + 1]
        # print('a=',a,'b=',b)
        temp = abs(x * y - a * b)
        list.append(temp)
    flag=False #标记是否有图片
    #print(list)
    for counter in range(-1,-(MAX_PIC_COUNT),-1):
        #print(-(MAX_PIC_COUNT))
        if list[counter]>MIN_PIC_SIZE:
            flag=True  #设置界限20000,表示有图片
            break
    if flag==False:
        return -1  #-1表示本文没有图片
    max = list[0]
    i = PIC_BEGIN
    for count in list:
        i += 1
        if count > max:
            max = count
            position = i

    #print('position=', position)
    return position
'''
def picCount(path,count_pic):
   dic = {}
   beginSize = 0
   tempSize = tempSize_1 = 0
   for i in range(1, count_pic):
      image1 = Image.open(path.format(i))
      dic[i] = picSize(image1)
   x, y = dic[count_pic-1]
   beginSize = x * y  # 初始大小
   x, y = dic[count_pic - 2]
   tempSize = beginSize - x * y  # 起始两个图片的大小
   beginSize = x * y
   for i in range(1, count_pic-2):
      x, y = dic[count_pic-2 - i]
      tempSize_1 = beginSize - x * y
      beginSize = x * y
      if tempSize > tempSize_1:
         return count_pic - i
'''
def picSize(image):
   w, h = image.size      #获得图片的大小（分辨率）
   return w, h
#保存下载的每张图片
def destFile(link,count,path):
    handler = urllib.request.ProxyHandler({'http': 'http://127.0.0.1:8087', 'https': 'http://127.0.0.1:8087'})
    opener = urllib.request.build_opener(handler)
    try:
        response = opener.open(link,timeout=TIMEOUT)
    except HTTPError as e:
        print('Error code',e.code)
        return
    name = path.format(count)
    f = open(name, 'wb')
    f.write(response.read())
    f.close()
    #print('Pic Saved!')
#返回一共下载了多少张图片
def downLoad(contentBytes,path):
    count_pic = 0  # 记录此次下载的总的图片数量
    #print(str(contentBytes))
    for link in re.findall(r'src="http[\S\s]{5,90}jpg', str(contentBytes)):
        #print(len(link),link[5:])
        link = link[5:]  # 去除网页中的src="这五个字符
        count_pic += 1
        destFile(link, count_pic,path)
    print("共有图片%d张" % count_pic)
     #只要最后八张图片
    picDelete(path,count_pic-MAX_PIC_COUNT)
    return count_pic
#转移正文图片到目的文件夹
def exchangePic(path,dest_path,begin_count,end_count):
    source_path=path
    dest_path_copy=dest_path
    global dest_path_count
    for i in range(begin_count,end_count+1):
        shutil.move(path.format(i), dest_path.format(dest_path_count))
        dest_path_count+=1
    pic_count=end_count-begin_count+1
    print("正文图片%d张"%pic_count)
def getAllUrl():
    global PIC_BEGIN
    path = "/Users/cp3/Desktop/pic/{0}.jpg"  # 网页下载图片的保存路径
    dest_path = "/Users/cp3/Desktop/pic_result/{0}.jpg"  # 正文图片保存路径
    proxies = {'http': 'http://127.0.0.1:8087', 'https': 'http://127.0.0.1:8087'}
    count_n = 0
    for line in open('url.txt'):
        PIC_BEGIN=1  #每个链接都初始化
        if re.search(r'dwnews', line):
            url = re.findall(r'http[\s\S]*?.html', line)[0]
            print('\n网址:', url)
            res = requests.get(url, proxies=proxies)
            contentBytes = res.text
            count_n += 1
            count=downLoad(contentBytes,path) #一共下载的图片个数
            if count==0:
                continue
            if count - MAX_PIC_COUNT>0:
                PIC_BEGIN = count - MAX_PIC_COUNT
            delete_count = picCount(path,count)  # 将多余的图片删除到count
            if delete_count==-1:
                print('正文没有图片')
                picDelete(path,count+1)
            else:
                picDelete(path, delete_count)
                exchangePic(path,dest_path,delete_count,count)
    print('共有此类网页 %d 个' % count_n)
#将一个指定网页的图片下载下来保存到本地
def getOneUrl(path):
    proxies = {'http': 'http://127.0.0.1:8087', 'https': 'http://127.0.0.1:8087'}
    url="https://www.boxun.com/news/gb/intl/2016/07/201607120059.shtml#.V5m8lZN96t8"
    try:
        res = requests.get(url, proxies=proxies)
    except HTTPError as e:
        print('Error code', e.code)
        return
    contentBytes = res.text
    return downLoad(contentBytes,path)
if __name__ == "__main__":
    getAllUrl()
    '''
    path = "/Users/cp3/Desktop/pic/{0}.jpg"  # 网页下载图片的保存路径
    dest_path = "/Users/cp3/Desktop/pic_result/{0}.jpg"  # 正文图片保存路径
    count=getOneUrl(path)
    PIC_BEGIN=count-MAX_PIC_COUNT
    #print('count=',count)
    delete_count = picCount(path, count)  # 将多余的图片删除到delete_count
    #print('delete_count=',delete_count)
    if delete_count==-1:  #没有图片
        print("正文没有图片")
        picDelete(path,count+1)
    else:
        picDelete(path, delete_count)  #删除到编号delete_count(不删除delete_count)
        #print('delete_couont=',delete_count,'count=',count)
        exchangePic(path, dest_path, delete_count, count)
    '''

