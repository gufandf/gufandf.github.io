import os
import time
import re
import _thread

try:
    from bs4 import BeautifulSoup
    import requests
except BaseException:
    print("缺失库:\nrequests\nbs4\n请尝试使用 'pip install' 命令安装")
    input(">>")


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
API = "https://api.loliurl.club/api/setu/?tag="

try:
    os.mkdir("download")
except FileExistsError:
    pass

tag = input("tag: ")
nember = int(input("nember: "))

global complete
global defeated
complete = 0
defeated = 0

def get_img(thread_name):
    html = requests.get(API+tag)
    html = BeautifulSoup(html.text,"lxml")
    try:
        img_a = str(html.find_all("a")[1])
        img_name = str(html.find_all("img")[0])
    except IndexError:
        global defeated
        defeated = defeated +1
        print("进度:(",complete,"/",nember,") 失败:",defeated)
        return
    img_url = re.findall('href="(.*?)"',img_a)[0]
    img_name = re.findall('alt="(.*?)"',img_name)[0]
    # print(thread_name,"号: ",img_url)
    download_img(img_url,img_name)

def download_img(url,name):
    global complete
    try:
        img = requests.get(url,headers=headers,timeout=50)
    except BaseException:
        global defeated
        defeated = defeated +1
        print("进度:(",complete,"/",nember,") 失败:",defeated)
        return
    f = open("download/"+name,"wb+")
    f.write(img.content)
    f.close()
    complete = complete + 1
    print("进度:(",complete,"/",nember,") 失败:",defeated)

print("分配任务...")

for i in range(nember):
    _thread.start_new_thread (get_img,(i,))
    time.sleep(0.1)

while nember > complete + defeated :
    pass
