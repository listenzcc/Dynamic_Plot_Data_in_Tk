# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from local_toolbox import Buffer, Plotter

plt.style.use('ggplot')
frame_rate = 20

buffer = Buffer()
buffer.push(np.random.randn(50, buffer.info['channels']))
buffer.display()


plotter = Plotter()
plotter.prepare_plot(max_length=buffer.info['max_length'],
                     channels=buffer.info['channels'])
plotter.plot(buffer.data)

plt.show(block=False)
plt.draw()

plt.pause(1 / frame_rate)

input('Press enter to start.')

for j in range(100):
    plotter.update(np.random.randn(1, buffer.info['channels']))

# input('Press enter to quit.')
