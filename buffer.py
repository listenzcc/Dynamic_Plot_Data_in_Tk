# coding: utf-8

import numpy as np


class Buffer():
    def __init__(self, length=100, interval=1):
        self.length = 100
        self.interval = 1
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
