#!/usr/bin/env python
#encoding=utf-8
 
from PIL import Image, ImageFilter, ImageDraw, ImageFont, ImageEnhance, ImageFilter

path="/Users/cp3/Desktop/pic/{0}.jpg"
def picSize(image):
   w, h = image.size      #获得图片的大小（分辨率）
   return w, h
def picCount():
   dic = {}
   list=[]
   pic_count=35
   for i in range(1, pic_count+1):
      image1 = Image.open(path.format(i))
      dic[i] = picSize(image1)
   print(dic)
   for i in range(1,pic_count):
      x , y = dic[i]
      #print(x,y)
      a , b = dic[i+1]
      #print('a=',a,'b=',b)
      temp=abs(x*y-a*b)
      list.append(temp)
   max=list[0]
   i=0
   for count in list:
      i+=1
      if count>max:
         max=count
         position=i+1
   print('position=',position)
if __name__=='__main__':
   picCount()
   #print("从第%d张开始:"%count)
