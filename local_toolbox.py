# coding: utf-8

import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt


class Buffer():
    def __init__(self, max_length=100, channels=13):
        self.info = {}
        self.data = np.zeros((max_length, channels))
        self.new_data = None

        self.comment('max_length', max_length)
        self.comment('channels', channels)

    def push(self, new_data):
        self.new_data = new_data
        self.data = np.concatenate((self.data, new_data))
        self.data = self.data[:self.info['max_length']]

    def pop(self):
        if self.new_data is None:
            return None
        out = self.new_data
        self.new_data = None
        return out

    def fetch(self, start=0, stop=0):
        return np.array(self.data[start:stop])

    def length(self):
        return len(self.data)

    def comment(self, key, value):
        self.info[key] = value

    def display(self):
        print('-' * 80)
        self.comment('_shape', self.data.shape)
        pprint(self.info)


class Plotter():
    def __init__(self, frame_rate=20):
        self.fig, self.axe = plt.subplots(1, 1, figsize=(5, 4), dpi=100)
        # self.fig = fig
        # self.axe = axe
        self.frame_rate = frame_rate
        # self.background = fig.canvas.copy_from_bbox(axe.bbox)

    def prepare_plot(self, max_length, channels):
        self.data = np.empty((0, channels))
        self.now = 0
        self.max_length = max_length

        self.lines = [e for e in range(channels)]
        for j in range(channels):
            self.lines[j] = self.axe.plot(self.data[:, j] + j, '-', alpha=0.8)

        self.axe.set_xlim([0, max_length-1])
        self.axe.set_ylim([-1, channels+1])
        self.axe.set_title('Init')

    def plot(self, data):
        self.data = data
        self.now = self.data.shape[0]
        self.lines = self.axe.plot(data, '-', alpha=0.8)

    def update(self, new_data):
        if new_data is None:
            return 0

        for j in range(new_data.shape[0]):
            self.now += 1
            self.now %= self.max_length
            self.data[self.now] = new_data[j]

        for j, line in enumerate(self.lines):
            line.set_ydata(self.data[:, j] + j)

        self.axe.redraw_in_frame()
        for line in self.lines:
            self.axe.draw_artist(line)

        self.fig.canvas.blit(self.axe.bbox)
