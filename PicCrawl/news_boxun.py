import re
count=0
for line in open('url.txt'):
    if re.search(r'epochtimes',line):
        count+=1
        print(line[2:])
print("此类网页 %d " % count)