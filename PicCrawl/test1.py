import requests as req
import re
resp=req.get(url="http://www.chinanews.com/gj/2016/07-21/7946623.shtml",timeout=3)
resp.encoding = "GDB"
html=resp.text
result=re.findall('正文',html)
print(result)
#result=re.findall(r'<[p]*>[\s\S]*</[p]*>',html)
#print(result)
#result1=re.findall(r'src=',result)
#print(result1)

