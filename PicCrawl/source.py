#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re

DBUG   = 0

reBODY = r'<body.*?>([\s\S]*?)<\/body>'
reCOMM = r'<!--.*?-->'
reTRIM = r'<{0}.*?>([\s\S]*?)<\/{0}>'
reTAG  = r'<[^p]*?>|[ \t\r\f\v]'

reIMG  = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>')
#url_globle='http://bbs.boxun.com/forum/201603/boxun2013/1952.shtml'


def doIt( url):
    print(url,'所含图片链接如下:\n')
    ext = Extractor(url=url, image=True)
    result = ext.getContext()
    #print(len(result))
    if len(result)==0:
        print('没有图片链接')
        return   #没有图片链接
    ext.findPicUrl(result[0])
class Extractor():
    def __init__(self, url = "", blockSize=3, timeout=5, image=True):
        self.url       = url
        self.blockSize = blockSize
        self.timeout   = timeout
        self.saveImage = image
        self.rawPage   = ""
        self.ctexts    = []
        self.cblocks   = []
    def getRawPage(self):
        try:
            proxies = {'http': 'http://127.0.0.1:8087', 'https': 'http://127.0.0.1:8087'}
            res = requests.get(self.url, proxies=proxies)
        except Exception as e:
            raise e

        if DBUG: print(res.encoding)

        res.encoding = "GBK"

        return res.status_code, res.text

    def processTags(self):
        self.body = re.sub(reCOMM, "", self.body)
        self.body = re.sub(reTRIM.format("script"), "" ,re.sub(reTRIM.format("style"), "", self.body))
        # self.body = re.sub(r"[\n]+","\n", re.sub(reTAG, "", self.body))
        self.body = re.sub(reTAG, "", self.body)
        print("body ",self.body)
    def processBlocks(self):
        self.ctexts   = self.body.split("\n")
        self.textLens = [len(text) for text in self.ctexts]

        self.cblocks  = [0]*(len(self.ctexts) - self.blockSize - 1)
        lines = len(self.ctexts)
        for i in range(self.blockSize):
            self.cblocks = list(map(lambda x,y: x+y, self.textLens[i : lines-1-self.blockSize+i], self.cblocks))

        maxTextLen = max(self.cblocks)

        if DBUG: print(maxTextLen)

        self.start = self.end = self.cblocks.index(maxTextLen)
        while self.start > 0 and self.cblocks[self.start] > min(self.textLens):
            self.start -= 1
        while self.end < lines - self.blockSize and self.cblocks[self.end] > min(self.textLens):
            self.end += 1

        #return "".join(self.ctexts[self.start:self.end])

        result = "".join(self.ctexts[self.start:self.end])
        result=re.findall(r"src=\S+jpg",result) #过滤出url
        return result

    def processImages(self):
        self.body = reIMG.sub(r'{{\1}}', self.body)
        #print("image   ",self.body)
    def getContext(self):
        code, self.rawPage = self.getRawPage()

        #print(self.rawPage,"code dlkfajdslkf")
        self.body = re.findall(reBODY, self.rawPage)[0]
        #print(self.body)
        if DBUG: print(code, self.rawPage)

        if self.saveImage:
            self.processImages()
        self.processTags()
        return self.processBlocks()
        # print(len(self.body.strip("\n")))
    def findPicUrl(self,context):
        url_jpg=re.findall('src=[\s\S]*?jpg',context)
        for i in range(len(url_jpg)):
            url_jpg[i]=url_jpg[i][4:]
            print(url_jpg[i])
if __name__ == '__main__':
    count=0
    '''
    for line in open('url.txt'):
        if re.search(r'dwnews', line):
            #print('网址:',line[2:])
            count+=1
            doIt(line[2:])'''
    doIt('http://www.backchina.com/forum/20160710/info-1394719-1-1.html')
    print('共有此类网页 %d 个' % count)
    #doIt('http://news.boxun.com/news/gb/yuanqing/2016/04/201604251125.shtml#.V5bDxJN976Y')