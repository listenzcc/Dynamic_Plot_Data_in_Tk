# coding: utf-8

'''
This a tkinter app to display waveforms in real time.
'''

import time
import numpy as np
import threading
import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from local_toolbox import Buffer


class App():
    def __init__(self, root, frame_rate=20):
        # Initialize root.
        self.root = root

        # Initialize frames.
        self.frames = dict(
            Figure=tk.Frame(root),  # Frame of figure.
            Control=tk.Frame(root),  # Frame of controls.
        )

        # Initialize buttons.
        self.buttons = dict(
            # Go button, start waveforms.
            Display=tk.Button(self.frames['Control']),
            # Quit button, close window.
            Quit=tk.Button(self.frames['Control']),
        )

        self.display_info = dict(
            frame_rate=frame_rate,  # Frame rate of animation.
            display_on=False,  # Display switcher.
            idx=0,  # Current vertical index.
            max_length=100,  # Max_length of display.
            channels=range(13),  # Channels to display.
            height=2,  # Height of each channel.
        )

        # Layout.
        self.layout()

        # Bound dynamic figure and buttons function.
        self.bounding()

    def layout(self):
        # Place frames.
        for name, frame in self.frames.items():
            print(name)
            frame.pack(side=tk.TOP)

        # Place buttons in control frame.
        for name, button in self.buttons.items():
            print(name)
            button.config(text=name)
            button.pack(side=tk.LEFT)

    def bounding(self):
        # Bound _quit function on Quit button.
        self.buttons['Quit'].config(command=self._quit)

        # Init buffer.
        buffer = Buffer()
        # buffer.push(np.random.randn(50, buffer.info['channels']))
        # buffer.print()

        # Plot using ggplot.
        # matplotlib.use('TkAgg')
        plt.style.use('ggplot')
        fig, axe = plt.subplots(1, 1, figsize=(5, 4), dpi=100)
        lines = dict()
        for j in self.display_info['channels']:
            lines[j] = axe.plot(self._biased(buffer.data, j), '-', alpha=0.8)
        axe.set_xlim([-1, buffer.info['max_length']])
        axe.set_ylim([-1, self.display_info['height']
                      * buffer.info['channels']])

        # Embed canvas on figure frame.
        canvas = FigureCanvasTkAgg(fig, master=self.frames['Figure'])
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # Embed on_key_event for key press on figure.
        canvas.mpl_connect('key_press_event', self.on_key_event)

        # Bound _start_thread function on Go button.
        self.buttons['Display'].config(command=self._realtime_display)

        self.buffer = buffer
        self.lines = lines
        self.fig = fig
        self.axe = axe

    def _biased(self, data, j):
        # Compute bias for j-th channel.
        bias = j * self.display_info['height']
        # Return biased data of j-th channel.
        return data[:, j] + bias

    def _start_thread(self):
        # Initialize and start thread for _run.
        p = threading.Thread(target=self._run)
        p.start()

    def _realtime_display(self):
        if self.display_info['display_on']:
            # Change button text into ON
            self.buttons['Display'].config(text='Display_ON')
            # Turn off display
            self.display_info['display_on'] = False
        else:
            # Change button text into OFF
            self.buttons['Display'].config(text='Display_OFF')
            # Turn on display
            self.display_info['display_on'] = True

        # Compute lag based on frame_rate.
        # lag is the time lag between frames.
        lag = 1 / self.display_info['frame_rate']

        # Begin dynamic display loop if display is on.
        while self.display_info['display_on']:
            # Stamp the frame begin.
            begin = time.time()

            # Update buffer.
            # TODO: The update buffer should be perform in a seperate thread.
            self.buffer.push(np.random.randn(np.random.randint(1, 5),
                                             self.buffer.info['channels']))

            # Read new_data from buffer.
            new_data = self.buffer.pop()
            if new_data is None:
                # Continue loop if no new_data.
                continue

            # Redraw background frame.
            self.axe.redraw_in_frame()

            for j, line in self.lines.items():
                # Update y_data of j-th line.
                # Get idx and data of the line.
                line_idx = self.display_info['idx']
                line_data = line[0].get_ydata()
                # Update line_data for each value in new_data.
                for x in self._biased(new_data, j):
                    line_data[line_idx] = x
                    # Update line_idx
                    line_idx += 1
                    line_idx %= self.display_info['max_length']
                # Write ydata of the line.
                line[0].set_ydata(line_data)

            # Updata vertical idx.
            self.display_info['idx'] = line_idx

            # Blit canvas.
            self.fig.canvas.blit(self.axe.bbox)
            # Flush canvas.
            self.fig.canvas.flush_events()

            if lag > (time.time() - begin):
                # Wait for remaining lagging time.
                time.sleep(lag - (time.time() - begin))
            else:
                # Report lagging, if a frame can not be updated on time.
                print('Lagging.')

    def on_key_event(self, event):
        # Handel key press.
        print('You pressed %s' % event.key)

    def _quit(self):
        self.display_info['display_on'] = False
        # Quit app and close window.
        self.root.quit()
        self.root.destroy()


matplotlib.use('TkAgg')
root = tk.Tk()
app = App(root)
root.mainloop()

print('Done!')
