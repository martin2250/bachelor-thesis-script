#!/usr/bin/python3
import argparse

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import scipy.signal

import lib.plotstyle

sample_rate = int(1e5)
duration = 10
N = int(duration * sample_rate)
time = np.linspace(0, duration, N)

signal_rms = 1
signal_frequency = 100
noise_rms = 1e-3
signal = np.sqrt(2) * signal_rms * np.sin(time * 2 * np.pi * signal_frequency)
noise = np.random.normal(scale=noise_rms * np.sqrt(sample_rate / 2), size=N)
voltage = signal + noise

fftresolution = sample_rate

# window = (windo function name, voltage correction factor)
# window = ('hamming'
window = 'hanning'			# correction factor: 1.5
# window = 'boxcar'

frequency, power = scipy.signal.welch(
    voltage, sample_rate, nperseg=fftresolution, window=window)

window_correction_factor = 1 / \
    np.mean(scipy.signal.get_window(window, fftresolution))

voltage = np.sqrt(power * 1.5)

print('factor: ', window_correction_factor)
print('peak:   ', voltage[int(signal_frequency * fftresolution / sample_rate)])

ax = plt.gca()
lib.plotstyle.format_bode_plot(ax)

ax.plot(frequency, voltage)

plt.show()
