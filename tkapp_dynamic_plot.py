# coding: utf-8

'''
This a tkinter app to display waveforms in real time.
'''

import time
import numpy as np
import threading
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from local_toolbox import Buffer


class App():
    def __init__(self, root, frame_rate=20):
        self.root = root
        # Initialize frames.
        self.frames = dict(
            Figure=tk.Frame(root),  # Frame of figure.
            Control=tk.Frame(root),  # Frame of controls.
        )
        # Initialize buttons.
        self.buttons = dict(
            # Go button, start waveforms.
            Display=tk.Button(self.frames['Control']),
            # Quit button, close window.
            Quit=tk.Button(self.frames['Control']),
        )

        self.display_info = dict(
            frame_rate=frame_rate,  # Frame rate of animation.
            display_on=False,  # Display switcher.
            idx=0,  # Current horizontal index.
            max_length=100,  # Max_length of display.
            channels=[5, 7, 9],  # Channels to display.
            height=2,  # Height of each channel.
        )

        # Layout.
        self.layout()

        # Bound dynamic figure and buttons function.
        self.bounding()

    def layout(self):
        # Place frames.
        for name, frame in self.frames.items():
            print(name)
            frame.pack(side=tk.TOP)

        # Place buttons in control frame.
        for name, button in self.buttons.items():
            print(name)
            button.config(text=name)
            button.pack(side=tk.LEFT)

    def bounding(self):
        # Bound _quit function on Quit button.
        self.buttons['Quit'].config(command=self._quit)

        # Init buffer.
        buffer = Buffer()
        # buffer.push(np.random.randn(50, buffer.info['channels']))
        # buffer.print()

        # Plot using ggplot.
        # matplotlib.use('TkAgg')
        plt.style.use('ggplot')
        fig, axe = plt.subplots(1, 1, figsize=(5, 4), dpi=100)
        lines = dict()
        for j in self.display_info['channels']:
            lines[j] = axe.plot(self._biased(buffer.data, j), '-', alpha=0.8)
        axe.set_xlim([-1, buffer.info['max_length']])
        axe.set_ylim([-1, self.display_info['height']
                      * buffer.info['channels']])

        # Embed canvas on figure frame.
        canvas = FigureCanvasTkAgg(fig, master=self.frames['Figure'])
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # Embed on_key_event for key press on figure.
        canvas.mpl_connect('key_press_event', self.on_key_event)

        # Bound _start_thread function on Go button.
        # self.buttons['Go'].config(command=self._run)
        self.buttons['Display'].config(command=self._realtime_display)

        self.buffer = buffer
        self.lines = lines
        self.fig = fig
        self.axe = axe

    def _biased(self, data, j):
        # Compute bias for j-th channels
        return data[:, j] + j * self.display_info['height']

    def _start_thread(self):
        # Initialize and start thread for _run.
        p = threading.Thread(target=self._run)
        p.start()

    def _realtime_display(self):
        if self.display_info['display_on']:
            self.buttons['Display'].config(text='Display_ON')
            self.display_info['display_on'] = False
        else:
            self.buttons['Display'].config(text='Display_OFF')
            self.display_info['display_on'] = True

        lag = 1 / self.display_info['frame_rate']

        while self.display_info['display_on']:
            begin = time.time()
            self.buffer.push(np.random.randn(1, self.buffer.info['channels']))

            self.axe.redraw_in_frame()
            new_data = self.buffer.pop()
            for j, line in self.lines.items():
                data = line[0].get_ydata()
                data[self.display_info['idx']] = self._biased(new_data, j)
                line[0].set_ydata(data)
            self.display_info['idx'] += 1
            self.display_info['idx'] %= self.display_info['max_length']

            self.fig.canvas.blit(self.axe.bbox)
            self.fig.canvas.flush_events()

            if lag > (time.time() - begin):
                time.sleep(lag - (time.time() - begin))

    def on_key_event(self, event):
        # Handel key press.
        print('You pressed %s' % event.key)

    def _quit(self):
        self.display_info['display_on'] = False
        # Quit app and close window.
        self.root.quit()
        self.root.destroy()


matplotlib.use('TkAgg')
root = tk.Tk()
app = App(root)
root.mainloop()

print('Done!')
