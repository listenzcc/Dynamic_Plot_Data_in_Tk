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
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvasAgg
from local_toolbox import Buffer, Plotter


class App():
    def __init__(self, root):
        self.root = root
        # Initialize frames.
        self.frames = dict(
            figure=tk.Frame(root),  # Frame of figure.
            control=tk.Frame(root),  # Frame of controls.
        )
        # Initialize buttons.
        self.buttons = dict(
            Go=tk.Button(root),  # Go button, start waveforms.
            Quit=tk.Button(root),  # Quit button, close window.
        )
        # Layout.
        self.layout()
        pass

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

        # Embed dynamic figure and buttons function.
        self.embedding()

    def embedding(self):
        # Bound _quit function on Quit button.
        self.buttons['Quit'].config(command=self._quit)

        # Init buffer.
        buffer = Buffer()
        buffer.push(np.random.randn(50, buffer.info['channels']))
        buffer.display()

        # Plot using ggplot.
        matplotlib.use('TkAgg')
        plt.style.use('ggplot')
        fig, axe = plt.subplots(1, 1, figsize=(5, 4), dpi=100)
        lines = axe.plot(buffer.data, '-', alpha=0.8)
        axe.set_ylim([-1, 15])
        axe.set_xlim([0, buffer.info['max_length'] * 3])

        # Embed canvas on figure frame.
        canvas = FigureCanvasAgg(fig, master=self.frames['figure'])
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # Embed on_key_event for key press on figure.
        canvas.mpl_connect('key_press_event', self.on_key_event)

        # Bound _start_thread function on Go button.
        self.buttons['Go'].config(command=self._run)
        # self.buttons['Go'].config(command=self._start_thread)

        self.buffer = buffer
        self.lines = lines
        self.fig = fig
        self.axe = axe

    def _start_thread(self):
        # Initialize and start thread for _run.
        p = threading.Thread(target=self._run)
        p.start()

    def _run(self):
        # Update plotter for 500 times.
        for j in range(500):
            print('-', j)
            t = time.time()
            self.buffer.push(np.random.randn(1, self.buffer.info['channels']))

            for i, line in enumerate(self.lines):
                line.set_ydata(self.buffer.data[:, i] + i)

            self.axe.redraw_in_frame()
            for line in self.lines:
                self.axe.draw_artist(line)
            # self.fig.canvas.draw()
            self.fig.canvas.blit(self.axe.bbox)
            self.fig.canvas.flush_events()
            # self.fig.canvas.blit(self.axe.bbox)
            # plt.pause(0.0001)
            print(time.time() - t)

    def on_key_event(self, event):
        # Handel key press.
        print('You pressed %s' % event.key)

    def _quit(self):
        # Quit app and close window.
        self.root.quit()
        self.root.destroy()


matplotlib.use('TkAgg')
root = tk.Tk()
app = App(root)
root.mainloop()

print('Done!')
