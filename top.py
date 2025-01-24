import markdown
import shutil, os, re, time

templatesRoot = "./site/templates/"
modelsRoot = "./models/"
postsRoot = "./site/p/"
siteRoot = "./site/"
buildRoot = "./docs/"

def coPath(path1: str, path2: str):
    path1 = path1.replace("./", "")
    path2 = path2.replace("./", "")
    path = path1.split("/")
    path.extend(path2.split("/"))
    path = "/".join(path)
    path = "./" + path
    return path


def readFileIn(root):
    d = {}
    for fileName in os.listdir(root):
        try:
            f = open(root + fileName, "r", encoding="UTF-8")
            d[fileName.split(".")[0]] = f.read()
            f.close()
        except PermissionError:
            pass
    return d

def walkPath(Path):
    files = []
    for fileOrg in os.walk(Path):
        for fileName in fileOrg[2]:
            filePath = fileOrg[0]+"/"+fileName
            files.append(filePath)
    return files

def buildFile(filePath):
    pass


def build():
    shutil.rmtree(buildRoot)
    shutil.copytree(siteRoot, buildRoot, True)

    templates = readFileIn(templatesRoot)
    # models = readFileIn(modelsRoot)

    # print("[build] building...")
    for fileOrg in os.walk(buildRoot):
        # print(f"[build] build {fileOrg}...")
        # fileOrg ('./build', ['p'], ['index copy.html', 'index.html'])
        for fileName in fileOrg[2]:
            fileType = fileName.split(".")[-1]
            if fileType == "html":
                f = open(coPath(fileOrg[0], fileName), "r", encoding="UTF-8")
                file = f.read()
                f.close()
                # 如果使用模板
                if len(re.findall('<template src=".+?">', file)) == 0:
                    break
                templateName = re.findall('<template src=".+?">', file)[0][15:-2]
                childs = re.findall('<child id="(.+?)">([^*]*?)</child>', file)
                # print("childs: "+json.dumps(childs))

                # 填充模版
                html = templates[templateName]
                for child in childs:
                    # print(child)
                    html = html.replace(f'{{{{{child[0]}}}}}', child[1])
                for child in re.findall("{{(.*?)}}", html):# 清除未填充的模版
                    html = html.replace(f'{{{{{child}}}}}', "") 
                f = open(coPath(fileOrg[0], fileName), "w", encoding="UTF-8")
                f.write(html)
                f.close()
            elif fileType == "md":
                f = open(coPath(fileOrg[0], fileName), "r", encoding="UTF-8")
                file = f.read()
                f.close()
                childs = {}
                for i in re.findall("<!-- (.*): (.*) -->", file):
                    childs[i[0]] = i[1].strip()
                childs["content"] = markdown.markdown(file,extensions=['markdown.extensions.toc','markdown.extensions.fenced_code','markdown.extensions.tables'])

                # 填充模版
                html = templates["base"]
                for child in childs:
                    html = html.replace(f'{{{{{child}}}}}', childs[child])
                for child in re.findall("{{(.*?)}}", html):# 清除未填充的模版
                    html = html.replace(f'{{{{{child}}}}}', "") 
                # print(re.findall("{{(.*?)}}", html)) # 清除未填充的模版
                f = open(coPath(fileOrg[0], fileName)[:-3]+".html", "w", encoding="UTF-8")
                f.write(html)
                f.close()
    print("<!> 构建完成|Build Complete")

watchList = {}
build()
# while True:
#     filePaths = walkPath(siteRoot)
#     for filePath in filePaths:
#         nowTime = f"{str(time.localtime().tm_hour).ljust(2,'0')}:{str(time.localtime().tm_min).ljust(2,'0')}:{str(time.localtime().tm_sec).ljust(2,'0')}"
#         try:
#             if watchList[filePath] != os.path.getmtime(filePath):
#                 print(nowTime+" [Change] "+filePath)
#                 watchList[filePath] = os.path.getmtime(filePath)
#                 build()
#         except FileNotFoundError:
#             print(nowTime+" [Change] "+filePath)
#             build()
#         except KeyError:
#             watchList[filePath] = os.path.getmtime(filePath)
#         except PermissionError:
#             print(nowTime+" [Error] 文件被占用: "+filePath)
#         except:
#             print(nowTime+" [Error] 未知错误: "+filePath)
#     time.sleep(1)
# build()
