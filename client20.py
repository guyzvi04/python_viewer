
def clientRun(contxtRun):
    print("Client running!!!")
    

    import queue
    import socket
    import os
    import threading
    import sys
    from servertest20 import get_ip
    from pynput.mouse import Controller,Button
    from pynput.keyboard import Key

    mouse = Controller()
    
    print(socket.gethostname())
    sys.path.append(os.getcwd())

    import pyautogui
    from vidstream import  ScreenShareClient
    from tkinter import END

    pyautogui.moveTo(x=0,y=0)



    ip_connect = get_ip(conTxt=contxtRun)  #ip from textbox
    

    def exe():
        while True:
            if executeQ:
                command = executeQ.get()
                
                commandlist = command.split('\n')

                char = commandlist[0]
                x = commandlist[1]
                y = commandlist[2]
                button = commandlist[3]

                
  
                if char != 'nan':
                    
                    try:
                        print(f'Typing - {char}')
                        char = str(char).replace("'","")
                        if len(char) == 1 or char.contains("space"):
                            pyautogui.typewrite(str(char))
                    except:
                        pass

                if x != 'nan' and y != 'nan':
                    try:
                        x = x.replace("nan","")
                        x = x.replace("'","")
                        y = y.replace("nan","")
                        y = y.replace("''","")
                        
                        if mouse.position != (x,y):
                            #print(f'Moving to - {x},{y}')
                            pyautogui.moveTo(x=int(x),y=int(y))
                    except:                    
                        pass  
                        #print("OUT OF BOUNDS")

                if button != "nan":
                    if 'left' in str(button):
                        pyautogui.click(button="left")
                        #print("clicked left")
                    elif 'right' in str(button):
                        pyautogui.click(button="right")
                        #print("clicked right")



                

    x = threading.Thread(target=exe)

    executeQ = queue.Queue()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((f'{ip_connect}', 8000))


    sender = ScreenShareClient(f'{ip_connect}',9999)
    tClient = threading.Thread(target=sender.start_stream)     #streaming

    x.start()
    tClient.start()

    while True:

        command = s.recv(1024).decode()
        executeQ.put(command)
        print("==========")
        print(command)
        print("==========")
        print("\n\n\n\n\n")
        
    

