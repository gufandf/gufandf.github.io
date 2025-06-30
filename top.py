import markdown
import shutil, os, re, time
import logging

templatesRoot = "./site/templates/"
modelsRoot = "./models/"
postsRoot = "./site/p/"
siteRoot = "./site/"
buildRoot = "./docs/"
modsRoot = "./site/mods/"


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
    fileType = filePath.split(".")[-1]
    target_filename = "./docs/"+"/".join(filePath.split("/")[2:]).split(".")[0]+".html"
    if fileType == "html":
        f = open(filePath, "r", encoding="UTF-8")
        file = f.read()
        f.close()
        # 如果使用模板
        if len(re.findall('<template src=".+?">', file)) == 0:
            return
        templateName = re.findall('<template src=".+?">', file)[0][15:-2]
        childs = re.findall('<child id="(.+?)">([^*]*?)</child>', file)
        # logging.info("childs: "+json.dumps(childs))

        # 填充模版
        html = templates[templateName]
        for child in childs:
            # logging.info(child)
            html = html.replace(f'{{{{{child[0]}}}}}', child[1])
        for child in re.findall("{{(.*?)}}", html):# 清除未填充的模版
            html = html.replace(f'{{{{{child}}}}}', "") 
        # 替换模组
        for mod in mods:
            html = html.replace(f"<mod src=\"{mod}\">",mods[mod])
        f = open(target_filename, "w", encoding="UTF-8")
        f.write(html)
        f.close()
    elif fileType == "md":
        f = open(filePath, "r", encoding="UTF-8")
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
        # logging.info(re.findall("{{(.*?)}}", html)) # 清除未填充的模版
        # 替换模组
        for mod in mods:
            html = html.replace(f"<mod src=\"{mod}\">",mods[mod])
        f = open(target_filename, "w", encoding="UTF-8")
        f.write(html)
        f.close()


def build():
    shutil.rmtree(buildRoot)
    shutil.copytree(siteRoot, buildRoot, True)

    # models = readFileIn(modelsRoot)

    for fileOrg in os.walk(buildRoot):
        # logging.info(f"[build] build {fileOrg}...")
        # fileOrg ('./build', ['p'], ['index copy.html', 'index.html'])
        for fileName in fileOrg[2]:
            buildFile(coPath(fileOrg[0], fileName))
    logging.info(nowTime+"构建完成")


templates = readFileIn(templatesRoot)
mods = readFileIn(modsRoot)

if __name__ == "__main__":
    watchList = {}
    nowTime = ""
    build()
    while True:
        nowTime = f"{str(time.localtime().tm_hour).ljust(2,'0')}:{str(time.localtime().tm_min).ljust(2,'0')}:{str(time.localtime().tm_sec).ljust(2,'0')}"
        filePaths = walkPath(siteRoot)
        for filePath in filePaths:
            try:
                if watchList[filePath] != os.path.getmtime(filePath):
                    logging.info(nowTime+" [Change] "+filePath)
                    watchList[filePath] = os.path.getmtime(filePath)
                    buildFile(filePath)
            except FileNotFoundError:
                logging.info(nowTime+"[Change]"+filePath)
                build()
            except KeyError:
                watchList[filePath] = os.path.getmtime(filePath)
            except PermissionError:
                # logging.warning(nowTime+"文件被占用: "+filePath)
                pass
            except:
                logging.warning(nowTime+"未知错误: "+filePath)
        time.sleep(3)
    # build()
