import os, json
with open("newdata.json", "r+", encoding="utf-8") as f:
    datas = json.load(f)
    datas = {}
    for folder in [fo for fo in os.listdir("AddedImagefolder")]:
        datas[folder] = []
        for name in [fo for fo in os.listdir("AddedImagefolder/" + folder)
                     if fo[-4:] != ".ini"]:
            datas[folder].append(name)
    f.truncate(0)
    print(datas)
    f.write(json.dumps(datas, indent=4))

            
