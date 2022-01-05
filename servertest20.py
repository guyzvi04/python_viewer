import socket
import os
import queue
import threading
from client20 import clientRun
import re
import time
import sys
import json
import ipaddress
import pyautogui
from requests import get

sys.path.append(os.getcwd())

import tkinter
from tkinter import END, Label
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Button, Listener as MouseListener
from pynput import keyboard
from pynput.mouse import Controller as mouse_controller
from vidstream import StreamingServer

mouse = mouse_controller()

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

start_time = time.time()
commands_q = queue.Queue()




def get_ip(conTxt):
    
    
    
    ip = conTxt.get("1.0","end-1c")

    if bool(re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)):
        conTxt.grid(row=1, column=1)
        return ip
    else:
        conTxt.delete('1.0', END)
        print("Wrong ip")


def mouse_handler():
    while True:
        command = mouse.position

        xTemp,yTemp = command[0],command[1]

        commandSend = f'nan\n{xTemp}\n{yTemp}\nnan'
        commands_q.put(commandSend)
        
        time.sleep(0.3)   


def on_press(key):
    command = f'{str(key)}\nnan\nnan\nnan'
    commands_q.put(command)

def on_click(x, y, button, pressed):
    if pressed:
        print(f'{button} pressed')
        command = f'nan\nnan\nnan\n{button}'
        commands_q.put(command)

def listenersSetup():
    keyboard_listener = KeyboardListener(on_press=on_press)
    mouse_listener = MouseListener(on_click=on_click)

    keyboard_listener.start()
    mouse_listener.start()
    keyboard_listener.join()
    mouse_listener.join()



def main():
    reciver = StreamingServer(f"{ip_address}",9999)
    tServer = threading.Thread(target=reciver.start_server) #screenShare handle
    tServer.start()
    
    x.start()
    y.start()
    soThread.start()

    
    

def run():
    pyautogui.moveTo(x=0,y=0)
    print("Server running!!!")
    sock =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind(('0.0.0.0',8000))
    sock.listen(1)
    status.configure(text='Waiting for connection...')
    status.grid(row=3,column=1)
    (clientSock,ClientAddress) = sock.accept()
    status.configure(text="Connected!",foreground="green")

    while True:
        if commands_q:
            cmd = commands_q.get()
            clientSock.send(str(cmd).encode('utf-8'))


if __name__ == "__main__":

    x = threading.Thread(target=listenersSetup)
    y = threading.Thread(target=run)
    soThread = threading.Thread(target=mouse_handler)



    root = tkinter.Tk()

    mode_name = ""

    def setup(screen:tkinter.Tk,mode_name):
        screen.geometry('280x120')
        screen.title(mode_name)

    setup(root,'temp')
    print(ip_address)

    con_label = tkinter.Label(root,text='Connect:').grid(row=0,column=0)
    slave_lebel = tkinter.Label(root,text='IPV4: ').grid(row=1,column=0)
    status = tkinter.Label(root,font=('arial',10, 'bold'),text="",foreground="blue")

    conTxt = tkinter.Text(root,width=10,height=2)
    conTxt.grid(row=0,column=1)

    slaveTxt = tkinter.Label(root, font=('arial', 16, 'bold'), text=f'{ip_address}', bd=16, anchor="w").grid(row=1, column=1)
    con_button = tkinter.Button(root,text='Connect',command=lambda: clientRun(conTxt)).grid(row=0,column=2)
    slave_button = tkinter.Button(root,text='Wait', command=lambda: main()).grid(row=1,column=2)


    root.mainloop()


