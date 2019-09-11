# coding: utf-8

import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt


class Buffer():
    '''
    This is a data buffer.
    '''
    def __init__(self, capacity=500, channels=13):
        # Information of the buffer.
        self.info = {}
        # Capacity of the buffer.
        self.comment('capacity', capacity)
        # Number of channels.
        self.comment('channels', channels)
        # Initialize buffer with capacity and channels.
        self.data = np.zeros((capacity, channels))
        # Initialize new_data.
        # new_data stores the lastest pushed data.
        self.new_data = None

    def push(self, new_data):
        # Push new_data into the buffer.
        # Use FIFO protocol to pervent the buffer exceeding capacity.
        # Temporary concatenate self.data and new_data.
        self.data = np.concatenate((self.data, new_data))
        # Shrink buffer back to its capacity.
        self.data = self.data[-self.info['capacity']:]
        # Storage new_data.
        self.new_data = new_data

    def pop(self):
        # Pop new_data since it storages lastest pushed data.
        if self.new_data is None:
            # If new_data is None, return None.
            return None
        # Set temporary variable out for new_data.
        out = self.new_data
        # Clear new_data.
        self.new_data = None
        # Return out.
        return out

    def fetch(self, start=0, stop=None):
        # Peek buffered data from start to stop.
        return self.data[start:stop]

    def length(self):
        # Return current length of the buffer.
        return len(self.data)

    def comment(self, key, value):
        # Record information.
        self.info[key] = value

    def print(self):
        # Print infomations.
        print('-' * 80)
        # _shape refers current shape of the buffered data.
        self.comment('_shape', self.data.shape)
        pprint(self.info)
