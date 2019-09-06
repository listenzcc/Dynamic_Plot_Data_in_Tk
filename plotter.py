# coding: utf-8

import numpy as np


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

        for j, line in enumerate(self.lines):
            line.set_ydata(self.data[:, j] + j)

        self.ax.redraw_in_frame()
        for line in self.lines:
            self.ax.draw_artist(line)

        self.fig.canvas.blit(self.ax.bbox)
