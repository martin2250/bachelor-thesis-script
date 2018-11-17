#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np
import numpy.fft
import scipy.signal

time = np.linspace(0, 1, int(1e5))
sample_rate = int(1e5)
voltage = np.sqrt(2) * 1 * np.sin(time * 2 * np.pi * 100)

N = len(voltage)
Nhalf = int(N / 2)

window = 1  # scipy.signal.hamming(int(1e5))

V_snake_n = 1 / N * numpy.fft.fft(voltage * window)[0:Nhalf]
J_f_n = N / sample_rate * np.abs(V_snake_n)**2 / N
Jss_f_n = 2 * J_f_n
spectral_power = np.sqrt(Jss_f_n)

# --> uV/sqrt(Hz)
spectral_power *= 1

print(spectral_power[99:102])
plt.plot(spectral_power)
plt.show()
