import markdown
import shutil, os, re
import json

templatesRoot = "./templates/"
modelsRoot = "./models/"
postsRoot = "./site/p/"

shutil.rmtree("./build")
shutil.copytree("./site", "./build", True)


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


templates = readFileIn(templatesRoot)
models = readFileIn(modelsRoot)

# print("templates: "+json.dumps(templates)+"\n")
# print("models: "+json.dumps(models)+"\n")

# post title headimg content

for fileOrg in os.walk("./build"):
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
                html = html.replace(f'{{{{{child[0]}}}}}', child[1])
            f = open(coPath(fileOrg[0], fileName), "w", encoding="UTF-8")
            f.write(html)
            f.close()
        elif fileType == "md":
            f = open(coPath(fileOrg[0], fileName), "r", encoding="UTF-8")
            file = f.read()
            f.close()
            print(file)
            childs = {}
            for i in re.findall("<!-- (.*): (.*) -->", file):
                childs[i[0]] = i[1].strip()
            childs["content"] = markdown.markdown(file,extensions=['markdown.extensions.toc','markdown.extensions.fenced_code','markdown.extensions.tables'])

            # 填充模版
            html = templates["base"]
            for child in childs:
                html = html.replace(f'{{{{{child}}}}}', childs[child])
            f = open(coPath(fileOrg[0], fileName)[:-3]+".html", "w", encoding="UTF-8")
            f.write(html)
            f.close()
