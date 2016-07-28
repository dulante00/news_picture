#下载网页中的图片到本地
import urllib.request
handler=urllib.request.ProxyHandler({'http': 'http://127.0.0.1:8087', 'https': 'http://127.0.0.1:8087'})
opener=urllib.request.build_opener(handler)
response=opener.open('http://pic2.dwnews.net/20160626/19ced3ecdc7abd68a894d48834bea18a_w_m.jpg')
name ='/Users/cp3/Desktop/3.jpg'
f=open(name,'wb')
f.write(response.read())
f.close()
print('Pic Saved!')