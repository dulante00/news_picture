#!/usr/bin/env python
#encoding=utf-8
 
import cStringIO, urllib2, Image
 
url = 'http://cdn.01happy.com/wp-content/uploads/2012/09/bg.png'
file = urllib2.urlopen(url)
tmpIm = cStringIO.StringIO(file.read())
im = Image.open(tmpIm)
 
print im.format, im.size, im.mode