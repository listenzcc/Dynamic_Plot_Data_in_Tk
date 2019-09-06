# coding: utf-8

import time
import numpy as np
import matplotlib.pyplot as plt


class Buffer():
    def __init__(self, length=100, interval=1):
        self.length = length
        self.interval = interval
        self.prepare()

    def prepare(self):
        self.x_data = np.arange(self.length) * self.interval
        self.y_data = np.zeros(self.length)

    def push(self, new_y_data):
        length = len(new_y_data)
        x_data = self.x_data[0] + \
            np.arange(self.length + length) * self.interval
        y_data = np.concatenate([self.y_data, new_y_data])
        self.x_data = x_data[-self.length:]
        self.y_data = y_data[-self.length:]


buffer = Buffer()

plt.style.use('ggplot')
# plt.ion()
frame_rate = 20

fig, axes = plt.subplots(2, 1)
background = fig.canvas.copy_from_bbox(axes[0].bbox)
line = axes[0].plot(buffer.x_data, buffer.y_data, '-o', alpha=0.8)
plt.show(False)
plt.draw()

plt.pause(1 / frame_rate)


for j in range(1000):
    buffer.push(np.random.randn(1))

    line[0].set_xdata(buffer.x_data)
    line[0].set_ydata(buffer.y_data)

    axes[0].set_xlim([buffer.x_data[0], buffer.x_data[-1]])

    new_min, new_max = min(buffer.y_data), max(buffer.y_data)
    axes[0].set_ylim([min(new_min, axes[0].get_ylim()[0]),
                      max(new_max, axes[0].get_ylim()[1])])

    t = time.time()
    # fig.canvas.restore_region(background)
    # redraw just the points
    axes[0].redraw_in_frame()
    axes[0].draw_artist(line[0])
    # fill in the axes rectangle
    fig.canvas.blit(axes[0].bbox)
    axes[0].set_title(j)
    time.sleep(1 / frame_rate)
    print(time.time() - t)

