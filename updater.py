import json, os
import PySimpleGUI as sg
from shizukani.image import Scraping
datafpath = "data.json"
encode = "utf-8"
with open(datafpath, "r", encoding=encode) as f:
    datas = json.loads(f.read())
sg.theme(datas["settings"]["theme"])
sg.set_options(font=(datas["settings"]["font"]["font"], datas["settings"]["font"]["size"]))
layout = [
    [sg.Text("JSONpath:"), sg.Input(key = "I1"), sg.FileBrowse("reference...")],
    [sg.Button("update",key="update"), sg.Button("close", key="close", button_color="red")],
    [sg.Push(),
      sg.Text("© 2024 NPO Challengepro,shizukani",
               font=(datas["settings"]["font"]["font"], datas["settings"]["font"]["size"]//2)),
      sg.Push()],
    ]
win = sg.Window("english app updater", layout)
while True:
    e, v = win.read()
    if e == "update":
        if not v["I1"] == "":
            with open(v["I1"], encoding=encode) as f2:
                datas["words"] = json.loads(f2.read())
            with open(datafpath, "w", encoding=encode) as f:
                f.write(json.dumps(datas, indent=4))
        elif not os.path.isfile(v["I1"]):
            sg.popup("指定されたファイルがありません。")
        words = []
        for category in datas["words"].values():
            for i in category:
                if not (i in words) : words.append(i)
        print(words, len(words))
        for file in os.listdir("images"):
            os.remove("images/" + file)
        for word in words:
            Scraping.fnamescraping(Scraping, word, word)
        
        sg.popup_ok("The update is complete. Do you want to close it?", title="close it?")
        e = "close"""
    if e == None or e == "close": break
win.Close()