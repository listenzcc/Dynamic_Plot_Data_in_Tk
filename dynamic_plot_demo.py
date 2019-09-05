# coding: utf-8

import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from buffer import Buffer

buffer = Buffer()

plt.style.use('ggplot')
plt.ion()
frame_rate = 20

fig, axes = plt.subplots(2, 1)
line = axes[0].plot(buffer.x_data, buffer.y_data, '-o', alpha=0.8)
plt.pause(1 / frame_rate)

for j in range(100):
    axes[0].set_title(j)
    buffer.push(np.random.randn(1))

    line[0].set_xdata(buffer.x_data)
    line[0].set_ydata(buffer.y_data)

    axes[0].set_xlim([buffer.x_data[0], buffer.x_data[-1]])

    new_min, new_max = min(buffer.y_data), max(buffer.y_data)
    axes[0].set_ylim([min(new_min, axes[0].get_ylim()[0]),
                      max(new_max, axes[0].get_ylim()[1])])

    try:
        plt.pause(1 / frame_rate)
    except tk._tkinter.TclError as TclError:
        print(TclError)
        break
