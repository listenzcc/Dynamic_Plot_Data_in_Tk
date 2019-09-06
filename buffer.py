# coding: utf-8

import time
import numpy as np
from pprint import pprint


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


if __name__ == '__main__':
    buffer = Buffer()
    buffer.display()
