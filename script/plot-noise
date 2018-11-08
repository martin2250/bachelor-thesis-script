#!/usr/bin/python3
import argparse

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import scipy.signal

import lib.plotstyle
import lib.tekdecode

parser = argparse.ArgumentParser(
    description='generates power density plots from time-domain oscilloscope data')
parser.add_argument('files', metavar='input_file', type=str, nargs='+',
                    help='csv/isf files from Tektronix scope')

args = parser.parse_args()

powers = []
sample_rate = None
frequency_total = None

for file in args.files:

    voltage, sample_rate_file, length = lib.tekdecode.loadFile(file)

    if sample_rate is None:
        sample_rate = sample_rate_file
    elif sample_rate_file != sample_rate:
        raise UserWarning(
            f'sample rate of file {file} ({sample_rate_file}) does not match sample rate of first file ({sample_rate})')

    frequency, power_squared = scipy.signal.welch(
        voltage, sample_rate, nperseg=100000)
    frequency_total = frequency

    power = np.sqrt(power_squared) * 1e6        # convert to µV/sqrt(Hz)
    powers.append(power)

print(powers)


ax = plt.gca()
lib.plotstyle.format_bode_plot(ax)

ax.plot(frequency_total, np.mean(powers, axis=0), label='file', alpha=0.7)

plt.show()
