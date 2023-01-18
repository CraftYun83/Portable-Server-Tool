from tkinter import *
import math, threading, subprocess, sys

root = Tk()
root.geometry(str(math.floor(root.winfo_screenwidth()/2))+"x"+str(math.floor(root.winfo_screenheight()/2)))

all_processes = []

terminal = Frame(root, width=root.winfo_screenwidth()/4, height=root.winfo_screenheight()/4)

canvas = Canvas(terminal, width=root.winfo_screenwidth()/4, height=root.winfo_screenheight()/4)
scrollbar = Scrollbar(terminal, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas, width=root.winfo_screenwidth()/4, height=root.winfo_screenheight()/4)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

terminal.pack(side=RIGHT, anchor=NE)

class MyThread(threading.Thread):
 
    # Thread class with a _stop() method.
    # The thread itself has to check
    # regularly for the stopped() condition.
 
    def __init__(self, *args, **kwargs):
        super(MyThread, self).__init__(*args, **kwargs)
        self._stop = threading.Event()
 
    # function using _stop function
    def stop(self):
        self._stop.set()
 
    def stopped(self):
        return self._stop.isSet()
 
    def run(self):
        process = subprocess.Popen(
            'java -jar craftbukkit-1.8.8-R0.1-SNAPSHOT-latest.jar nogui',
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            encoding='utf-8',
            errors='replace'
        )

        while True:
            realtime_output = process.stdout.readline()

            if realtime_output == '' and process.poll() is not None:
                break

            if realtime_output:
                Label(scrollable_frame, text=realtime_output.strip()).pack(anchor=NW)

def wipe_terminal():
    for process in all_processes:
        process.stop()
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    terminalThread = MyThread()
    terminalThread.start()
    all_processes.append(terminalThread)

terminalThread = MyThread()
terminalThread.start()
all_processes.append(terminalThread)

controlPanel = Frame(root, width=root.winfo_screenwidth()/4, height=root.winfo_screenheight()/4)

Button(controlPanel,text="Restart Server", command=wipe_terminal).pack()

controlPanel.pack(side=LEFT, anchor=NW)

root.mainloop()