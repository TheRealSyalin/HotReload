from sys import argv
from selenium import webdriver
from os import walk
from time import sleep
import os
import tkinter

running = True
path_to_track = "project path"
url = ""

if len(argv) > 1:
     path_to_track = argv[1]

file_dirs = {path_to_track: float(1)}

window = tkinter.Tk()
window.geometry("600x200")
window.title("Hot Reload")


def Close():
     global running 
     
     driver.quit()
     window.destroy()
     running = False

window.protocol("WM_DELETE_WINDOW", Close)
window.protocol("WM_CLOSE", Close)

path_field = tkinter.Text(window, height = 1, width = 40)
path_field.pack()
path_field.insert(tkinter.END, path_to_track)

url_field = tkinter.Text(window, height = 1, width = 40)
url_field.pack()
url_field.insert(tkinter.END, "url")


driver = webdriver.Chrome()

def CollectFiles():
    global path_to_track, file_dirs

    if not os.path.exists(path_to_track):
         return
    
    file_dirs.clear()
    file_dirs[path_to_track] = os.stat(path_to_track).st_mtime
    path = path_to_track
    

    for (path, dirnames, filenames) in walk(path):
            for file in filenames:
                if str(file).endswith(tuple([".html", ".js", ".css"])):
                    file_dirs[path + "\\" + file] = os.stat(path + "\\" + file).st_mtime

    #for k in file_dirs:
         #print(k + "\n")


def TryConnect():
    global path_to_track, url

    path_to_track = path_field.get("1.0", 'end-1c')
    url = url_field.get("1.0", 'end-1c')

    if not os.path.exists(path_to_track):
         return
    
    CollectFiles()
    
    try:
        driver.get(url)
    except Exception as ex:
        return


button = tkinter.Button(window, text="Connect", command=TryConnect)
button.place(x=250, y=100)
       

def Application():
    global path_to_track

    
    check = True
    while running:
        

        if not os.path.exists(path_to_track):
            window.update_idletasks()
            window.update()
            sleep(0.1)
        else:    
            k, v = list(file_dirs.items())[0]
            if not v == os.stat(k).st_mtime:
                    CollectFiles()
                    driver.refresh()
            for key in file_dirs:
                if not file_dirs[key] == os.stat(key).st_mtime:
                    print(key + " updated")
                    file_dirs[key] = os.stat(key).st_mtime
                    driver.refresh()

        window.update_idletasks()
        window.update()
        sleep(0.1)


if __name__ == "__main__":
    Application()
     
     

