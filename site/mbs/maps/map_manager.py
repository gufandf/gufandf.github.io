import requests
import os
import json
import logging

url_tree = "https://gitee.com/api/v5/repos/gufandf/mc-maps/git/trees/{}"
url_file = "https://gitee.com/api/v5/repos/gufandf/mc-maps/git/blobs/{}"


maps_json_exists = os.path.exists("./maps.json")
if maps_json_exists:
    maps_json = json.loads(open("./maps.json","r",encoding="UTF-8").read())
else:
    maps_json = []

all_map_files = []

def get_tree(url):
    r = requests.get(url)
    if r.status_code == 200:
        return json.loads(r.content)
    else:
        logging.error(url+"请求失败")
        return {}

def gitee_walk(url,path=""):
    files = []
    for i in get_tree(url)["tree"]:
        if i["type"] == "tree":
            files += gitee_walk(i["url"],i["path"]+"/")
        if i["type"] == "blob":
            files.append({"filename":i["path"],"filepath":path+i["path"],"url":i["url"]})
    return files

a = gitee_walk(url_tree.format("master"))
for i in a:
    print(i)