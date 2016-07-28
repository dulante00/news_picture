import os
filename='/Users/cp3/Desktop/pic/1.jpg'
if os.path.exists(filename):  #检查指定文件是否存在
    os.remove(filename)        #存在则删除
    print("删除成功！\n")
else:
    print("文件不存在！\n")