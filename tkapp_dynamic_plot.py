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
    def __init__(self, root, frame_rate=20, record_rate=30, num_channels=15):
        # Initialize root.
        self.root = root
        self.num_channels = num_channels

        # Initialize frames.
        self.frames = dict(
            Figure=tk.Frame(root),  # Frame of figure.
            Control=tk.Frame(root),  # Frame of controls.
            Status=tk.Frame(root),  # Frame of status.
            Selector=tk.Frame(root),  # Frame of selectors.
        )

        # Initialize buttons.
        self.buttons = dict(
            # Display button, toggle display.
            Display=tk.Button(self.frames['Control']),
            # Record button, toggle record.
            Record=tk.Button(self.frames['Control']),
            # Quit button, close window.
            Quit=tk.Button(self.frames['Control']),
        )

        # Initialize labels.
        self.labels = dict(
            # Display status label.
            Display=tk.Label(self.frames['Status']),
            # Record status label.
            Record=tk.Label(self.frames['Status']),
        )

        # Initialize selectors.
        self.selectors = dict()
        for j in range(num_channels):
            self.selectors[j] = [tk.Checkbutton(
                self.frames['Selector']), tk.IntVar()]

        # Initialize record parameters.
        self.recorder_info = dict(
            buffer=Buffer(num_channels=self.num_channels),  # Buffer of data.
            record_rate=record_rate,  # Record rate.
            record_on=False,  # Record switcher.
        )

        # Initialize display parameters.
        self.displayer_info = dict(
            frame_rate=frame_rate,  # Frame rate of animation.
            display_on=False,  # Display switcher.
            idx=0,  # Current vertical index.
            max_length=100,  # Length to display.
            channels=range(self.num_channels),  # Channels to display.
            height=2,  # Height of each channel.
        )

        # Layout the tkinter GUI.
        self.layout()

        # Bound dynamic figure and buttons function.
        self.bounding()

        # Overwrite onclose function for safety quit.
        self.root.protocol('WM_DELETE_WINDOW', self._quit)

    def layout(self):
        # Place frames.
        for name, frame in self.frames.items():
            print(name)
            frame.pack(side=tk.TOP)

        # Place buttons in control frame.
        for name, button in self.buttons.items():
            print(name)
            button.config(text=name)
            button.pack(side=tk.LEFT, padx=5, pady=1)

        # Place labels in status frame.
        for name, label in self.labels.items():
            print(name)
            label.config(text=name)
            label.pack(side=tk.LEFT, padx=5, pady=1)

        # Place selectors in selectors frame.
        for idx, selector in self.selectors.items():
            print(idx)
            selector[0].config(text=idx, variable=selector[1])
            selector[0].grid(row=idx // 5, column=idx % 5)
            selector[1].set(1)

    def _selectors_change(self):
        self.displayer_info['channels'] = [
            name for name, selector in self.selectors.items()
            if selector[1].get() == 1]

    def bounding(self):
        # Bound _quit function on Quit button.
        self.buttons['Quit'].config(command=self._quit)

        # Bound _selectors_change function on selectors.
        for selector in self.selectors.values():
            selector[0].config(command=self._selectors_change)

        # Init buffer.
        buffer = self.recorder_info['buffer']

        # Plot using ggplot.
        # matplotlib.use('TkAgg')
        plt.style.use('ggplot')
        fig, axe = plt.subplots(1, 1, figsize=(5, 4), dpi=100)
        data = np.zeros((self.displayer_info['max_length'],
                         buffer.info['num_channels']))
        lines = dict()
        for j in self.displayer_info['channels']:
            lines[j] = axe.plot(self._biased(data, j), '-', alpha=0.8)
        axe.set_xlim([-1, self.displayer_info['max_length']])
        axe.set_ylim([-1, self.displayer_info['height']
                      * buffer.info['num_channels']])

        # Embed canvas on figure frame.
        canvas = FigureCanvasTkAgg(fig, master=self.frames['Figure'])
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # Embed on_key_event for key press on figure.
        canvas.mpl_connect('key_press_event', self.on_key_event)

        # Bound toggle function on Record button.
        self._toggle_record(init=True)
        self.buttons['Record'].config(command=self._toggle_record)
        # Start recording thread.
        self._start_thread(self._realtime_record)

        # Bound _realtime_display function on Display button.
        self.buttons['Display'].config(text='Display_ON')
        self.labels['Display'].config(bg='red')
        self.displayer_info['display_on'] = False
        self.buttons['Display'].config(command=self._realtime_display)
        # Follow is components used for _realtime_display function.
        self.lines = lines
        self.fig = fig
        self.axe = axe

    def _biased(self, data, j):
        # Compute bias for j-th channel.
        bias = j * self.displayer_info['height']
        # Return biased data of j-th channel.
        return data[:, j] + bias

    def _toggle_record(self, init=False):
        if init:
            # Change button text into ON.
            self.buttons['Record'].config(text='Record_ON')
            self.labels['Record'].config(bg='red')
            # Turn off record.
            self.recorder_info['record_on'] = False
            return 0
        # Toggle record.
        if self.recorder_info['record_on']:
            # Change button text into ON.
            self.buttons['Record'].config(text='Record_ON')
            self.labels['Record'].config(bg='red')
            # Turn off record.
            self.recorder_info['record_on'] = False
        else:
            # Change button text into OFF.
            self.buttons['Record'].config(text='Record_OFF')
            self.labels['Record'].config(bg='green')
            # Turn off record.
            self.recorder_info['record_on'] = True

    def _start_thread(self, target):
        # Initialize and start background thread.
        # Recording function.
        p = threading.Thread(target=target)
        p.start()

    def _realtime_record(self):
        # A thread that records real-time feedings.
        # Start itself.
        self._realtime_record_on = True
        # Print starts.
        print('Recording process starts.')
        # Compute lag between updates.
        lag = 1 / self.recorder_info['record_rate']
        # Loop until self._realtime_record_on becomes False.
        buffer = self.recorder_info['buffer']
        while self._realtime_record_on:
            # Fetch some data here.
            new_data = np.random.randn(np.random.randint(1, 5),
                                       buffer.info['num_channels'])
            if self.recorder_info['record_on']:
                # Record if record_on.
                buffer.push(new_data)
            else:
                # Do nothing.
                pass
            # Wait lag until next update.
            time.sleep(lag)
        # Print stops.
        print('Recording process stops.')

    def _realtime_display(self):
        # Toggle display.
        if self.displayer_info['display_on']:
            # Change button text into ON.
            self.buttons['Display'].config(text='Display_ON')
            self.labels['Display'].config(bg='red')
            # Turn off display.
            self.displayer_info['display_on'] = False
        else:
            # Change button text into OFF.
            self.buttons['Display'].config(text='Display_OFF')
            self.labels['Display'].config(bg='green')
            # Turn on display.
            self.displayer_info['display_on'] = True

        if not self.displayer_info['display_on']:
            return 0

        # Compute lag based on frame_rate.
        # lag is the time lag between frames.
        lag = 1 / self.displayer_info['frame_rate']
        print('Display starts')
        # Begin dynamic display loop if display is on.
        buffer = self.recorder_info['buffer']
        while self.displayer_info['display_on']:
            # Stamp the frame begin.
            begin = time.time()

            # Read new_data from buffer.
            new_data = buffer.pop()
            if new_data is None:
                # Continue loop if no new_data.
                self.fig.canvas.flush_events()
                continue

            # Redraw background frame.
            self.axe.redraw_in_frame()

            for j, line in self.lines.items():
                if j in self.displayer_info['channels']:
                    line[0].set_visible(True)
                else:
                    line[0].set_visible(False)
                    continue
                # Update y_data of j-th line.
                # Get idx and data of the line.
                line_idx = self.displayer_info['idx']
                line_data = line[0].get_ydata()
                # Update line_data for each value in new_data.
                for x in self._biased(new_data, j):
                    line_data[line_idx] = x
                    # Update line_idx
                    line_idx += 1
                    line_idx %= self.displayer_info['max_length']
                # Write ydata of the line.
                line[0].set_ydata(line_data)

            # Updata vertical idx.
            self.displayer_info['idx'] = line_idx

            # Blit canvas.
            self.fig.canvas.blit(self.axe.bbox)
            # Flush canvas.
            self.fig.canvas.flush_events()

            if lag > (time.time() - begin):
                # Wait for remaining lagging time.
                time.sleep(lag - (time.time() - begin))
            else:
                # Report lagging, if a frame can not be updated on time.
                print('Delay happens.')
        # Loop stops means display stops.
        print('Display stops')

    def on_key_event(self, event):
        # Handel key press.
        print('You pressed %s' % event.key)

    def _quit(self):
        # Stop display thread.
        self.displayer_info['display_on'] = False
        # Stop recording thread.
        self._realtime_record_on = False
        # Quit app and close window.
        self.root.quit()
        self.root.destroy()


matplotlib.use('TkAgg')
root = tk.Tk()
app = App(root)
root.mainloop()

print('Done!')
