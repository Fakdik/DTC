import tkinter as tk
import tkinter.filedialog as fd

import shutil
import os

from configparser import ConfigParser

CONFIG_FILE = "./config.cfg"
SEPARATOR = ";"
config = ConfigParser()
dt =  os.path.expanduser("~\\Desktop")

if not os.path.isfile(CONFIG_FILE):
    config["DEFAULT"] = {
        "DesktopFolder": dt,
        "LockedFiles": ""
    }
    config["USER"] = {
        "DesktopFolder": dt,
        "LockedFiles": ""
    }
    try:
        with open(CONFIG_FILE, "w") as f:
            config.write(f)
    except Exception:
        print(Exception)
else:
    config.read(CONFIG_FILE)

root = tk.Tk()

def getFolder():
    config.read(CONFIG_FILE)

    directory = fd.askdirectory(title="Открыть папку", initialdir="./")
    if directory:
        config["USER"]["DesktopFolder"] = directory
        re()

        try:
            with open(CONFIG_FILE, "w") as f:
                config.write(f)
        except Exception:
            print(Exception)

def onSelect(ev):
    elems = []
    for i in ev.widget.curselection():
        elems.append(ev.widget.get(i))

    locked = SEPARATOR.join(elems)
    config.read(CONFIG_FILE)
    config["USER"]["LockedFiles"] = locked

    try:
        with open(CONFIG_FILE, "w") as f:
            config.write(f)
    except Exception:
        print(Exception)

def exterminate():
    if config["USER"]["DesktopFolder"] == "": return False
    
    path = config["USER"]["DesktopFolder"]
    locked = config["USER"]["LockedFiles"].split(SEPARATOR)

    for f in os.listdir(path):
        if f in locked: continue
        fullpath = path + "/" + f

        if os.path.isdir(fullpath):
            shutil.rmtree(fullpath)
        else:
            os.remove(fullpath)

    re()

def re():
    listWidget.delete(0, tk.END)

    path = config["USER"]["DesktopFolder"] \
        if config["USER"]["DesktopFolder"] != "" \
        else config["DEFAULT"]["DesktopFolder"]

    locked = config["USER"]["LockedFiles"].split(SEPARATOR)

    for file in os.listdir(path):
        listWidget.insert(tk.END, file)

        if file in locked:
            listWidget.select_set(tk.END)

def generateBat():
    path = config["USER"]["DesktopFolder"] \
        if config["USER"]["DesktopFolder"] != "" \
        else config["DEFAULT"]["DesktopFolder"]

    locked = config["USER"]["LockedFiles"].split(SEPARATOR)

    files = []
    dirs = []
    for p in os.listdir(path):
        fullpath = path + "/" + p
        if p not in locked:
            if os.path.isdir(fullpath):
                dirs.append(p)
            elif os.path.isfile(fullpath):
                files.append(p)
    print (files)
    print(dirs)

    unfi = open("unlocked_files.txt", "w+")
    undi = open("unlocked_dirs.txt","w+")

    for file in files:
        if file == 0:
            break
        else:
            unfi.write('\"%s\"' % file)
            unfi.write("\n") 
    for fold in dirs:
        if fold == 0:
            break
        else:
            undi.write('\"%s\"' % fold)
            undi.write("\n") 
    unfi.close()
    undi.close()

    cmd = "chcp 1251\n"
    cmd += "echo @off\n"
    cmd += "cd \"%s\"\n" % os.path.abspath(__file__).replace(os.path.basename(__file__),'')

    cmd += 'FOR /f "usebackq delims=" %%%%a IN ("unlocked_files.txt") DO del /f /q %s\\%%%%a)\n' % path
    cmd += 'FOR /f "usebackq delims=" %%%%b IN ("unlocked_dirs.txt") DO rd /s /q %s\\%%%%b\n' % path

    # rm -f !(file.txt|data.dat)
    try:
        with open("desktop_cleaner.bat", "w") as f:
            f.write(cmd)
    except Exception:
        print(Exception)





root.title("DTCleaner")
root.geometry("400x450")  

mainmenu = tk.Menu(root)
root.config(menu=mainmenu)

filemenu = tk.Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Указать папку", command=getFolder)

mainmenu.add_cascade(label="Настройки", menu=filemenu)

listWidget = tk.Listbox(root, selectmode=tk.MULTIPLE,	width = root.winfo_screenwidth(),
														height = len(dt)//2)

re()

listWidget.bind('<<ListboxSelect>>', onSelect)
listWidget.pack()

btn = tk.Button(text="Очистить", command=exterminate)
btn.pack(side='bottom')
btn = tk.Button(text="Автозагрузка", command=generateBat)
btn.pack(side='bottom')

root.mainloop()
