import os

list=os.listdir('/Users/cp3/Desktop/pic')
print(list)
for file in list:
    metadata=os.stat('/Users/cp3/Desktop/pic/{0}'.format(file))
    print(metadata.st_size)

