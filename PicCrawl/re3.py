import re
count=0
for line in open('url.txt'):
    if re.search(r'ntdtv', line):
        url=re.findall(r'http[\s\S]*?.html',line)
        print('网址:', url,len(url))
        count += 1
print('count=',count)