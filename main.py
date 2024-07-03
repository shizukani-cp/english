import PySimpleGUI as sg
from PIL import Image
import os, glob, json
import pyttsx3

try:
    import gtts, playsound
except ImportError:
    pass

datafpath = "data.json"
f = open(datafpath, "r", encoding="utf-8")
datas = json.loads((f.read()))
f.close()
word = datas["words"]
category = tuple(word.keys())[0]
index=0

if not datas["settings"]["internet"]:
    engine = pyttsx3.init()
    engine.setProperty('rate', datas["settings"]["speed"])
    engine.setProperty("volume", datas["settings"]["volume"])
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)

sg.theme(datas["settings"]["theme"])
sg.set_options(font=(datas["settings"]["font"]["font"], datas["settings"]["font"]["size"]))
layout=[
    [sg.Listbox(list(word.keys()), size=(12, 8), enable_events=True, k="categories"),
     sg.Button("←", k="back"), sg.Image(k="photo"), sg.Button("→", k="next")],
    [sg.Input("", key="I1", size=(12, 1)), sg.Button("spell", k="B1", bind_return_key=True), sg.Text("", k="spell")],
    [sg.Button("say", k="B2")],
    [sg.Button("アプリを終了", k="B3", button_color="red")],
    [sg.Push(),
      sg.Text("© 2024 NPO Challengepro,shizukani",
               font=(datas["settings"]["font"]["font"], datas["settings"]["font"]["size"]//2)),
      sg.Push()],
    ]

def shownext(win, index, category):

    try:
        os.remove("audio.mp3")
    except:
        pass

    fname = glob.glob("images/" + word[category][index] + ".*")[0]
    img = Image.open(fname)
    img.thumbnail((300, 200))
    ftmp = 'tmp.png'
    img.save(ftmp)
    win["photo"].update(filename=ftmp)
    win["spell"].update("")
    win["I1"].update("")

win = sg.Window("Image English", layout=layout, finalize=True)

shownext(win, index, category)

while True:
    e, v = win.read()
    if e == None or e == "B3": break
    if e == "back":
        index -= 1
        index %= len(word[category])
        shownext(win, index, category)
    if e == "next":
        index += 1
        index %= len(word[category])
        shownext(win, index, category)
    if e == "categories":
        category = v["categories"][0]
        index = 0
        shownext(win, index, category)
    if e == "B1":
        if v["I1"] != "":
            if v["I1"] == word[category][index]:
                win["spell"].update("Correct! " + word[category][index])
            else:
                win["spell"].update("Uncorrect... " + word[category][index])
        else:
            win["spell"].update(word[category][index])
    if e == "B2":
        if datas["settings"]["internet"]:
            gtts.gTTS(word[category][index]).save("_tmp.mp3")
            playsound.playsound("_tmp.mp3")
            os.remove("_tmp.mp3")
        else:
            engine.say(word[category][index])
            engine.runAndWait()

win.Close()