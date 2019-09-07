
import time
import threading
import tkinter as tk


class App():
    def __init__(self, root):
        self.button = tk.Button(root)
        self.button.pack()
        self._resetbutton()

    def _resetbutton(self):
        self.running = False
        self.button.config(text="Start", command=self.startthread)

    def startthread(self):
        self.running = True
        newthread = threading.Thread(target=self.printints)
        newthread.start()
        self.button.config(text="Stop", command=self._resetbutton)

    def printints(self):
        x = 0
        while self.running:
            print(x)
            x += 1
            time.sleep(1)  # Simulate harder task


root = tk.Tk()

app = App(root)

root.mainloop()
