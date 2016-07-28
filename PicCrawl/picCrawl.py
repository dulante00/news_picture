#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re


DBUG   = 0

#reTAG  = r'<[\s\S]*?>|[ \t\r\f\v]'
#http://military.people.com.cn/n1/2016/0724/c1011-28580193.html
#http://news.boxun.com/news/gb/yuanqing/2016/04/201604251121.shtml
reIMG  = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>')
url_globle=''

'''
def getHuml():
    proxies = {'http': 'http://127.0.0.1:8087', 'https': 'http://127.0.0.1:8087'}
    res = requests.get(url_globle, proxies=proxies)
    print(res.text)
'''


def GetPicUrl( src):
    # print('出始网址',src)
    if  src.__contains__('http://') or src.__contains__('https://'):
        src = src[src.index('h'):]
    elif src.__contains__('com'):
        if src[0]=='"' or src[0]=="'":
            src=src[1:]
        src='http:'+src
    else:
        count = src.index('/')
        src = src[count:]
        comCount = url_globle.index('com')
        src = url_globle[:comCount + 3] + src
        # print("最终网址", src)
    return src
def doIt( url):

    ext = Extractor(url=url, image=True)
    result = ext.getContext()
    #print('result::::::',result)
    #print(len(result))
    #print('结果:',result)
    #return
    if  result==None:
        return
    if len(result)==0 :
        print('没有图片链接')
        return   #没有图片链接
    else:
        print('所含图片链接如下:')
        #print("result:",result)
        #picResult = re.sub(r'http[\S]*?gif', "", result)
        #picResult = re.sub(r'http[\S]*?html', "", result)
        #print('picResult',result)
        picResult = re.findall(r'src=[\S]*?\.jpg', result)
        for picResultText in picResult:
            #print(picResultText[4:])
            print(GetPicUrl(picResultText[4:]))
class Extractor():
    def __init__(self, url = "", timeout=50, image=False):
        self.url=url
        #self.blockSize=blockSize
        self.timeout= timeout
        self.saveImage = image
        self.rawPage= ""
        self.ctexts= []
        self.cblocks= []
    def chineseLeng(self,text):
        text = re.findall(r'[\u4e00-\u9fa5]', text)
        return len(text)
    def getRawPage(self):
        try:
            proxies = {'http': 'http://127.0.0.1:8087', 'https': 'http://127.0.0.1:8087'}
            res = requests.get(self.url, proxies=proxies)
        #print(res.text)
        except Exception as e:
            raise e
        self.ctexts = res.text.split("\n")
        if DBUG: print(res.encoding)
        #注意网页的编码格式

        for i in range(1,20):
            if re.search('gb2312',self.ctexts[i]):
                res.encoding = "gb2312"
                break
            else:
                res.encoding="utf-8"
                break
        #res.encoding = "utf-8"
    def getContentBeginEnd(self):
        begin=end=rowCount=0 #开始标记和结束标记,行号标记的初始化
        tempBegin=tempEnd=0 #临时的开始,结束标记的记录
        count=0
        for text in self.ctexts:
            if re.search(r'meta',text):
                self.ctexts[count]=""
            count+=1
        flag=0
        flag_begin=0
        for text in self.ctexts:
            rowCount+=1
            if begin==0 and self.chineseLeng(text)>50: #找首个正文的切入点
                begin=rowCount
                flag_begin=1
                #print('begin:::::',begin,text)
                tempBegin=rowCount
            if (rowCount-tempBegin)>20 and self.chineseLeng(text)<30 and flag==0 and flag_begin==1:
                flag=1
                end=rowCount  #开始位置移动
            if self.chineseLeng(text) > 30:
                tempBegin = rowCount
                #print('tempBegin::::', tempBegin)
            #if self.chineseLeng(text)<50:
              #  tempBegin=rowCount
        begin = begin - 20 #避免图片前后的误差
        end = end + 10
        print('begin:',begin,'end:',end)
        #print(self.ctexts[88])
        #print(self.chineseLeng(self.ctexts[240]))
        count=0
        tempText=""
        for text in self.ctexts:
            count+=1
            if begin<count and count<end:
                #print(text)
                tempText+=text
        #print('tempText=',tempText)

        return tempText

    def DownPic(PicUrl):
        print("good")
    def getContext(self):
        self.getRawPage()
        if DBUG: print(self.rawPage)
        #return self.processBlocks
        return self.getContentBeginEnd()
        #print(len(self.body.strip("\n")))

    def getUrl(self):
        readFile=open("url.txt")


if __name__ == '__main__':
    #cout=0
    #getHuml()
    '''
    count = 0
    for line in open('url.txt'):
        if re.search(r'ntdtv', line):
            url=re.findall(r'http[\s\S]*?.html',line)[0]
            print('\n网址:',url)
            url_globle=url  #记录此次的网址
            count += 1
            if url=='https://www.boxun.com/news/gb/intl/2016/07/201607120059.shtml':
                pass
            else:
                doIt(url)

    print('共有此类网页 %d 个' % count)
    '''
    #ext = Extractor(url=url_globle,image=True)
    #ext.getContext()
    url_globle = 'http://www.ntdtv.com/xtr/gb/2016/07/12/a1275624.html'
    doIt('http://www.ntdtv.com/xtr/gb/2016/07/12/a1275624.html')