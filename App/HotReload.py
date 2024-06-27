from sys import argv
from selenium import webdriver
from os import walk
from time import sleep
import os
import tkinter

running = True

path_to_track = "Invalid"

if len(argv) > 1:
     path_to_track = argv[1]

file_dirs = {}

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

text = tkinter.Text(window, height = 1, width = 40)
text.pack()
text.insert(tkinter.END, path_to_track)

driver = webdriver.Chrome()

try:
    driver.get(path_to_track)
except Exception as ex:
    path_to_track = "Invalid"

def CollectFiles():
    global path_to_track
    path = path_to_track

    for (path, dirnames, filenames) in walk(path):
            for file in filenames:
                if str(file).endswith(tuple([".html", ".js", ".css"])):
                    file_dirs[path + "\\" + file] = os.stat(path + "\\" + file).st_mtime

    for k in file_dirs:
         print(k + "\n")
    

def Application():

    global path_to_track
    
    while path_to_track == "Invalid":
        path_to_track = text.get("1.0", 'end-1c')
        try:
             driver.get(path_to_track)
        except Exception as ex:
             path_to_track = "Invalid"

        window.update_idletasks()
        window.update()
        sleep(0.1)

    driver.get(path_to_track)
    file_dirs[path_to_track] = os.stat(path_to_track).st_mtime
    CollectFiles()

    while running:
        if not file_dirs[path_to_track] == os.stat(path_to_track).st_mtime:
             CollectFiles()

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
     
     

