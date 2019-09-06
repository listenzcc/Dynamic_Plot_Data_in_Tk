# coding: utf-8

import numpy as np
import tkinter as tk
import matplotlib
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

from plotter import Plotter
from buffer import Buffer

import multiprocessing


def on_key_event(event):
    print('you pressed %s' % event.key)
    key_press_handler(event, canvas)


def _quit(root):
    root.quit()
    root.destroy()


matplotlib.use('TkAgg')
root = tk.Tk()
root.title('matplotlib in TK')

figure_frame = tk.Frame(root)
figure_frame.pack(side=tk.TOP)

control_frame = tk.Frame(root)
control_frame.pack(side=tk.TOP)

fig = Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=figure_frame)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
canvas.mpl_connect('key_press_event', on_key_event)

button = tk.Button(master=control_frame, text='Quit',
                   command=lambda r=root: _quit(r))
button.grid(row=0, column=1, padx=2, pady=0)

button = tk.Button(master=control_frame, text='Go')
button.grid(row=0, column=0, padx=2, pady=0)

t = arange(0.0, 3, 0.01)
s = sin(2*pi*t)
axe = fig.add_subplot(2, 1, 1)
axe.plot(t, s)

buffer = Buffer()
buffer.push(np.random.randn(50, buffer.info['channels']))
buffer.display()

plotter = Plotter(fig, axe)
plotter.prepare_plot(max_length=buffer.info['max_length'],
                     channels=buffer.info['channels'])
plotter.plot(buffer.data)


def run():
    for j in range(500):
        plotter.update(np.random.randn(1, buffer.info['channels']))


button['command'] = run

tk.mainloop()
