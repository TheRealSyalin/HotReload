from sys import argv
from sys import platform
from selenium import webdriver
from os import walk
from time import sleep
from FileWatcher import FileWatcher
import os
import tkinter
import signal

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
     
     running = False

signal.signal(signal.SIGTERM, Close)
window.protocol("WM_DELETE_WINDOW", Close)

path_field = tkinter.Text(window, height = 1, width = 40)
path_field.pack()
path_field.insert(tkinter.END, path_to_track)

url_field = tkinter.Text(window, height = 1, width = 40)
url_field.pack()
url_field.insert(tkinter.END, "url")


driver = webdriver.Chrome()

def TryConnect():
    global path_to_track, url

    path_to_track = path_field.get("1.0", 'end-1c')
    url = url_field.get("1.0", 'end-1c')

    if not os.path.exists(path_to_track):
         return
    
    try:
        driver.get(url)
    except Exception as ex:
        return


button = tkinter.Button(window, text="Connect", command=TryConnect)
button.place(x=250, y=100)
       

def Application():
    global path_to_track

    fw = FileWatcher()
    check = True
    while running:
        

        if os.path.exists(path_to_track):
            if not fw.ob.is_alive():
                fw.ob.schedule(fw, path_to_track, recursive=True)
                fw.ob.start()

                print(fw.ob.is_alive())

            if fw.is_modified:
                    driver.refresh()

            print(fw.is_modified)
            fw.is_modified = False
        window.update_idletasks()
        window.update()
        sleep(0.1)
    
    driver.quit()
    window.destroy()
    fw.ob.stop()
    fw.ob.join()

if __name__ == "__main__":
    Application()
     
    

