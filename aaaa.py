
import numpy as np
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
# dummy data
N      = 100
buffer = np.zeros((N, 2))
p = ax.plot(*buffer.T, marker = '.')[0] # get plot object
plt.show(block=False)
while True:
    print('-')
    for idx in range(N):
        print('.')
        buffer[idx, :] = np.random.rand(buffer.shape[1])
        p.set_data(*buffer.T)
        # recompute data limits
        ax.relim()
        ax.axes.autoscale_view(True, True, True)

        # update figure; flush events
        fig.canvas.draw()
        fig.canvas.flush_events()