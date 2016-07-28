#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re

DBUG   = 0

reBODY = r'<body.*?>([\s\S]*?)<\/body>'
reCOMM = r'<!--.*?-->'
reTRIM = r'<{0}.*?>([\s\S]*?)<\/{0}>'
reTAG  = r'<[^p]*?>|[ \t\r\f\v]'
#reTAG  = r'<[\s\S]*?>|[ \t\r\f\v]'
#http://military.people.com.cn/n1/2016/0724/c1011-28580193.html
#http://news.boxun.com/news/gb/yuanqing/2016/04/201604251121.shtml
reIMG  = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>')
url_globle='http://www.backchina.com/forum/20160710/info-1394719-1-1.html'

'''
def getHuml():
    proxies = {'http': 'http://127.0.0.1:8087', 'https': 'http://127.0.0.1:8087'}
    res = requests.get(url_globle, proxies=proxies)
    print(res.text)
'''
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
            print(picResultText[5:])
class Extractor():
    def __init__(self, url = "", timeout=50, image=False):
        self.url=url
        #self.blockSize=blockSize
        self.timeout= timeout
        self.saveImage = image
        self.rawPage= ""
        self.ctexts= []
        self.cblocks= []

    def getRawPage(self):
        try:
            proxies = {'http': 'http://127.0.0.1:8087', 'https': 'http://127.0.0.1:8087'}
            res = requests.get(self.url, proxies=proxies)
        #print(res.text)
        except Exception as e:
            raise e

        if DBUG: print(res.encoding)

        res.encoding = "utf-8"

        return res.status_code, res.text

    def processTags(self):
        self.body = re.sub(reCOMM, "", self.body)
        self.body = re.sub(reTRIM.format("script"), "" ,re.sub(reTRIM.format("style"), "", self.body))
        # self.body = re.sub(r"[\n]+","\n", re.sub(reTAG, "", self.body))
        self.body = re.sub(reTAG, "", self.body)
        self.ctexts = self.body_resource.split("\n")  # 用回车分开
        '''
        count=0
        for i in range(0,len(self.ctexts)):
            count+=1
            print(count,'  ',self.ctexts[i])
        '''
        #print('self.ctexts',self.ctexts[350])
        #self.body=re.sub(r'[a-zA-Z\d<>=":;,-./\'()!\{}?&_%|$#]*',"",self.body)  #去除所有的标签和英文,只留下汉字内容,以便来查找正文
        #print('body',self.body,'body')

    def getContentBeginEnd(self):
        content = re.sub(r'[a-zA-Z\d<>=":;,-./\'()!\{}?&_%|$#]*', "", self.body)
        begin=end=rowCount=0 #开始标记和结束标记,行号标记的初始化
        tempBegin=tempEnd=0 #临时的开始,结束标记的记录
        content=content.split("\n")
        for text in content:
            rowCount+=1
            if begin==0 and len(text)>20: #找首个正文的切入点
                begin=rowCount
                tempBegin=rowCount
            if len(text)>80 or (rowCount-tempBegin)<20:
                if len(text)>80:
                    tempBegin=rowCount
            end=tempBegin

        #print('主体::::::',self.body)
        tempContent=self.body.split('\n')
        #print(tempContent)
        #print('第50行::::::::',tempContent[352])
        count=0
        tempText=""
        for text in self.ctexts:
            count+=1
            if begin<count and count<end:
                #print(text)
                tempText+=text
        #print('tempText=',tempText)
        return tempText
    def GetPicUrl(self, src):
        #print('出始网址',src)
        if not src.__contains__('http://'):
            count = src.index('/')
            src = src[count:]
            comCount = url_globle.index('com')
            src = url_globle[:comCount +3]+src
            #print("最终网址", src)
        else:
            src=src[src.index('h'):]
        return src
    def DownPic(PicUrl):
        print("good")
    def processImages(self):
        self.body = reIMG.sub(r'{{\1}}', self.body)

    def getContext(self):
        code, self.rawPage = self.getRawPage()
        self.body_resource = re.findall(reBODY, self.rawPage)[0]
        self.body=re.findall(reBODY, self.rawPage)[0]
        if DBUG: print(code, self.rawPage)

        if self.saveImage:
            self.processImages()
        self.processTags()
        #return self.processBlocks
        return self.getContentBeginEnd()
        #print(len(self.body.strip("\n")))

    def getUrl(self):
        readFile=open("url.txt")


if __name__ == '__main__':
    #cout=0
    #getHuml()

    count = 0

    for line in open('url.txt'):
        if re.search(r'molihua', line):
            url=re.findall(r'http[\s\S]*?.html',line)[0]
            print('\n网址:',url)
            count += 1
            doIt(url)

    #doIt('http://www.molihua.org/2016/07/blog-post_316.html')
    print('共有此类网页 %d 个' % count)
    '''
    ext = Extractor(url=url_globle,image=True)
    ext.getContext()
    '''