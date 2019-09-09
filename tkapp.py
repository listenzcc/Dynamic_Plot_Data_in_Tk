# code: utf-8
'''
This is a demo code for using threading module in python tkinter.
The key conception is embedding multi-threading func and tkinter root
into a single class.
'''

import time
import threading
import tkinter as tk
from pprint import pprint


class App():
    def __init__(self, root):
        # Setup root and buttons.
        self.root = root
        self.buttons = dict(
            start=tk.Button(root),  # Start a thread.
            list=tk.Button(root),  # List threads.
            stop=tk.Button(root),  # Stop oldest thread.
        )
        # Initialize threads dict storages informations of threads.
        self.threads = dict()
        # Place buttons and bind functions.
        self.init_components()

    def init_components(self):
        # Place butons, just pack, no layout.
        for name, button in self.buttons.items():
            print(name)
            button.config(text=name)
            button.pack()

        # Bind thread functions.
        self.buttons['start'].config(command=self._start_thread)
        self.buttons['list'].config(command=self._list_threads)
        self.buttons['stop'].config(command=self._stop_thread)

        # Stop threads and destory root.
        def on_closing():
            while self._stop_thread():
                pass
            self.root.destroy()

        # Bind close functions.
        self.root.protocol('WM_DELETE_WINDOW', on_closing)

    def _stop_thread(self):
        # Stop oldest thread.
        for name in self.threads.keys():
            # Set lifetime to 0, so printints will stop automatically.
            if self.threads[name]['lifetime']:
                self.threads[name]['lifetime'] = 0
                # Return 1 if one thread is stopped.
                return 1
        # Reaching here means there are no threads running.
        # Return 0.
        return 0

    def _start_thread(self):
        # Make a name for the thread to be started.
        # Names are naturally unique,
        # however I hope there are not too many threads.
        # I know the limitation of threads is stupid,
        # but the demo may not be too complicated, since it can do nothing.
        if len(self.threads) > 65536:
            raise('Too many threads exists, can not start new thread.')
            return 1
        name = '_thread_%d' % len(self.threads)
        # Initialize the thread.
        newthread = threading.Thread(target=self.printints,
                                     kwargs={'name': name},
                                     name=name)
        # Add the thread to the threads dict.
        self.threads[name] = dict(lifetime=10, instance=newthread)
        # Report the thread start.
        print('%s starts' % name)
        # Start the thread.
        newthread.start()
        # Return 0 if everything is fine.
        return 0

    def _list_threads(self):
        # List all threads.
        pprint(self.threads)

    def printints(self, name):
        # Custom print function.
        # Initialize x.
        x = 0
        # Loop until no lifetime.
        while self.threads[name]['lifetime'] > 0:
            # Consume lifetime.
            self.threads[name]['lifetime'] -= 1
            # Print name and x.
            print(name, x)
            # x increases.
            x += 1
            # Simulate a harder task.
            time.sleep(1)
        # Report when the thread stops.
        print('%s stops.' % name)


# Setup tkinter master.
root = tk.Tk()

# Instantiate App.
app = App(root)

# App starts.
root.mainloop()
