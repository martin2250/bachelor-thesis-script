#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt

(T, R) = np.loadtxt('calibration.dat', unpack=True)

plt.plot(T, R)
plt.show()
