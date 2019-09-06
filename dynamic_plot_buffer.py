# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from buffer import Buffer

plt.style.use('ggplot')
frame_rate = 20

buffer = Buffer()

buffer.push(np.random.randn(50, buffer.info['channels']))

buffer.display()


class Plotter():
    def __init__(self, fig, ax, frame_rate=20):
        self.fig = fig
        self.ax = ax
        self.frame_rate = frame_rate
        self.background = fig.canvas.copy_from_bbox(ax.bbox)

    def prepare_plot(self, max_length, channels):
        self.data = np.empty((0, channels))
        self.now = 0
        self.max_length = max_length

        self.lines = [e for e in range(channels)]
        for j in range(channels):
            self.lines[j] = self.ax.plot(self.data[:, j] + j, '-', alpha=0.8)

        self.ax.set_xlim([0, max_length-1])
        self.ax.set_ylim([-1, channels+1])
        self.ax.set_title('Init')

    def plot(self, data):
        self.data = data
        self.now = self.data.shape[0]
        self.lines = self.ax.plot(data, '-', alpha=0.8)

    def update(self, new_data):
        if new_data is None:
            return 0

        for j in range(new_data.shape[0]):
            self.now += 1
            self.now %= self.max_length
            self.data[self.now] = new_data[j]

        print(self.now)

        for j, line in enumerate(self.lines):
            line.set_ydata(self.data[:, j] + j)

        self.ax.redraw_in_frame()
        for line in self.lines:
            self.ax.draw_artist(line)
        self.fig.canvas.blit(self.ax.bbox)


fig, axes = plt.subplots(1, 1)
plotter = Plotter(fig, axes, frame_rate=frame_rate)
plotter.prepare_plot(max_length=buffer.info['max_length'],
                     channels=buffer.info['channels'])
plotter.plot(buffer.data)

plt.show(block=False)
plt.draw()

plt.pause(1 / frame_rate)

# input('Press enter to start.')

for j in range(5000):
    plotter.update(np.random.randn(1, buffer.info['channels']))

input('Press enter to quit.')
