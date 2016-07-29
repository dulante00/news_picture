#!/usr/bin/env python
#_*_coding:utf-8_*_
import shutil
import re
import requests.packages.urllib3.util.ssl_
import os
import requests
CURRENT_URL=''
LINK_LIST=[]        #存放网页中图片地址的链接
TIMEOUT=50          #请求超时记录
#MIN_PIC_SIZE=20000  #用于筛选较小的无用图片
MAX_PIC_COUNT=8     #每个网页最多保留的图片个数
PIC_BEGIN=1
URL_FILE_PATH='/Users/cp3/PycharmProjects/PicCrawl/url.txt'     #存放url的文件位置
DEST_FILE_PATH='/Users/cp3/Desktop/pic_result/{0}'              #最终新闻正文图片的保存位置
FILE_PATH='/Users/cp3/Desktop/pic'                              #图片保存的文件夹
PIC_PATH='/Users/cp3/Desktop/pic/{0}'                           #图片的保存路径

#删除指定名字图片
def picDelete(filename):
    file_path=PIC_PATH.format(filename)
    if os.path.exists(file_path):         # 检查指定文件是否存在
        os.remove(file_path)              # 存在则删除
        #print('删除图片:',file_path)
    else:
        print("文件不存在!")

#保存下载的每张图片
def destFile(link):
    proxies={'http': 'http://127.0.0.1:8087', 'https': 'http://127.0.0.1:8087'}
    fileName = link.split('/').pop()       #取最后的标识符
    img = requests.get(link, proxies=proxies, verify=False).content
    f = open(PIC_PATH.format(fileName), 'wb')
    f.write(img)
    f.close()
def cleanMorePic():
    max_range = 0                         # 最大幅度差距的两张图片
    index = 0                             # 大小差距最大两张图片的位置
    list_pic={}
    list_pic_name=[]
    list_pic_name=os.listdir(FILE_PATH)   #图片列表
    if len(list_pic_name)==1:             #网页中没有多余图片
        return
    for pic in list_pic_name[1:]:
        metadata=os.stat(PIC_PATH.format(pic))
        list_pic.setdefault(metadata.st_size,pic)
    list_pic = sorted(list_pic.items(), key=lambda list_pic: list_pic[0], reverse=True)
    if list_pic==None or len(list_pic)==0: #网页中没有多余图片
        return
    else:
        pre_pic_size,value=list_pic[0]
        count=0
        for list in list_pic:
            count+=1
            key,value=list
            range=abs(key-pre_pic_size)     #两张图片大小的差值
            if range>max_range:
                max_range=range
                index=count
            pre_pic_size=key
        count=0
        for list in list_pic:
            count+=1
            key,value=list
            if count>=index:
                picDelete(value)

#若图片多余MAX_PIC_COUNT清除冗余的图片
def cleanSurplusPic():
    list_pic={}                                       #保存此网页图片大小的列表 key:图片大小,value:图片名
    list_pic_name=os.listdir(FILE_PATH)               #此次的图片列表
    #print(list_pic_name)
    for pic in list_pic_name[1:]:
        metadata=os.stat(PIC_PATH.format(pic))        #图片的元数据
        list_pic.setdefault(metadata.st_size,pic)     #图片大小和图片名的字典
    list_pic=sorted(list_pic.items(),key=lambda list_pic:list_pic[0],reverse=True)        #图片按大小从大到小排序
    pic_count=len(list_pic_name)-1
    if pic_count>MAX_PIC_COUNT:                        #将多余的图片删除到最多只剩MAX_PIC_COUNT张
        count=0
        for item in list_pic:
            count+=1
            if count>MAX_PIC_COUNT:
                key,delete_pic_name=item
                picDelete(delete_pic_name)

#返回一共下载了多少张图片
def downLoad(contentBytes):
    count_pic = 0     # 记录此次下载的总的图片数量
    global LINK_LIST  #每次初始化列表
    LINK_LIST=[]
    for link in re.findall(r'src=[\S\s]{5,90}\.jpg', str(contentBytes)):
        link = urlAutoComplete(link[5:])                #去除网页中的src="这五个字符
        count_pic += 1
        LINK_LIST.append(link)                          #将链接加入到列表中
        destFile(link)                                  #以图片的url来命名图片
    print("共有图片%d张" % count_pic)
                                                        #只要最后八张图片
    if count_pic>MAX_PIC_COUNT:                         #如果图片个数大于MAX_PIC_COUNT只留MAX_PIC_COUNT张图片
        cleanSurplusPic()

#转移正文图片到目的文件夹
def movPic():
    global PIC_PATH
    global FILE_PATH
    global DEST_FILE_PATH
    list_pic_name=os.listdir(FILE_PATH)
    for pic in list_pic_name[1:]:
        shutil.move(PIC_PATH.format(pic), DEST_FILE_PATH.format(pic))

#URL自动补全
def urlAutoComplete(url):
    if not url.__contains__('http'):                     #检测到图片链接不完整
        comCount = CURRENT_URL.index('com')
        url = CURRENT_URL[:comCount + 3] + url
    return url

#将一个指定网页的图片下载下来保存到本地
def getOneUrl(path):
    global CURRENT_URL
    proxies = {'http': 'http://127.0.0.1:8087', 'https': 'http://127.0.0.1:8087'}
    CURRENT_URL="http://www.ntdtv.com/xtr/gb/2016/07/17/a1276571.html"
    try:                                                  #关闭证书校验
        res = requests.get(CURRENT_URL, proxies=proxies,verify=False)
    except TimeoutError:
        print('Request TimeOut')
    contentBytes = res.text
    downLoad(contentBytes)

#读取文件中的url进行测试
def getAllUrl():
    proxies = {'http': 'http://127.0.0.1:8087', 'https': 'http://127.0.0.1:8087'}
    count_n = 0
    for line in open(URL_FILE_PATH):
        if re.search(r'dwnews', line):
            url = re.findall(r'http[\s\S]*?.html', line)[0]
            print('\n网址:', url)                            #关闭证书校验
            res = requests.get(url, proxies=proxies,verify=False)
            contentBytes = res.text
            count_n += 1
            downLoad(contentBytes)                           #一共下载的图片个数
            cleanMorePic()
            movPic()
    print('共有此类网页 %d 个' % count_n)
if __name__ == "__main__":
    getAllUrl()
    #getOneUrl(PIC_PATH)
    #cleanMorePic()
    #movPic()



