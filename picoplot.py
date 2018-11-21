#!/usr/bin/python
import importlib
import math
import time
from ctypes import *

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import picoscope
import scipy.optimize
from picoscope import ps6000

# picoscope = importlib.reload(picoscope)
# ps6000 = importlib.reload(ps6000)

ps = ps6000.PS6000()


def setFreq(freq):
	offsetVoltage = 0.0
	pkToPk = 0.3
	m = ps.lib.ps6000SetSigGenBuiltInV2(
		c_int16(ps.handle),
		c_int32(int(offsetVoltage * 1000000)),
		c_int32(int(pkToPk * 1000000)),
		c_int16(0),
		c_double(freq), c_double(freq),
		c_double(0.0), c_double(0.0), c_uint(0), c_uint(0),
		c_uint32(0xFFFFFFFF), c_uint32(0),  # shots, sweeps
		# c_uint32(100), c_uint32(0),	#shots, sweeps
		c_uint(0), c_uint(0),
		c_int16(0))
	if m != 0:
		raise Exception("error setting freq: " + str(m) + " at freq " + str(freq))


def sine(t, a, f, phi, b):
	return a * np.sin(f * 2 * np.pi * t - phi) + b


def fitsine(X, Y, freq):
	maxY = np.max(np.abs(Y))
	if maxY == 0:
		maxY = 0.01
	guess = [maxY, freq, 0, 0]  # amplitude, frequency, phase
	(a, f, p, b), pconv = scipy.optimize.curve_fit(sine, X, Y, guess,
                                                bounds=(
                                                    [0, freq * 0.8, 0, -2],
                                                    [maxY * 1.1, freq * 1.2, 2 * np.pi, 2]))
	return a, f, p, b


#vranges = [50e-3, 100e-3, 200e-3, 500e-3, 1.0, 2.0, 5.0, 10.0, 20.0]
vranges = [range['rangeV'] for range in ps.CHANNEL_RANGE]
vranges = [0.000001] + vranges
rangeA = 5
rangeB = 5

ps.setChannel(channel="A", coupling="DC",
              VRange=vranges[rangeA], probeAttenuation=1.0)
ps.setChannel(channel="D", coupling="DC",
              VRange=vranges[rangeB], probeAttenuation=1.0)
ps.setSimpleTrigger("A", threshold_V=0)
ps.setNoOfCaptures(1)

samples = 10000

fmin = 0.1
fmax = 100e3
fnum = 100


flogmin = np.log(fmin)
flogmax = np.log(fmax)

floglist = np.linspace(flogmin, flogmax, fnum)

flist = np.exp(floglist)

gain = np.zeros(fnum)
phase = np.zeros(fnum)
err = np.zeros(fnum)


for i in range(0, len(flist)):
	i = len(flist) - 1 - i
	f = flist[i]
	setFreq(f)
	time.sleep(0.01)
	sf = ps.setSamplingFrequency(f * 6000, samples)[0]

	repeat = True
	count = 0
	lineA = None

	while repeat and count < len(vranges) + 1:
		repeat = False
		count = count + 1
		ps.runBlock()
		ps.waitReady()

		dataA = ps.getDataV("A")
		dataB = ps.getDataV("D")

		# plt.clf()
		# plt.plot(dataA, label='A')
		# plt.plot(dataB, label='B')
		# plt.show()

		T = np.arange(len(dataA)) / sf

		aA, fA, pA, bA = fitsine(T, dataA, f)
		aB, fB, pB, bB = fitsine(T, dataB, f)

		maxA = np.max(np.abs(dataA))
		maxB = np.max(np.abs(dataB))

		if(rangeA > 0 and maxA < 0.6 * vranges[rangeA - 1]):
			rangeA = rangeA - 1
			ps.setChannel(channel="A", coupling="DC",
			              VRange=vranges[rangeA], probeAttenuation=1.0)
			repeat = True

		if(rangeB > 0 and maxB < 0.6 * vranges[rangeB - 1]):
			rangeB = rangeB - 1
			ps.setChannel(channel="D", coupling="DC",
			              VRange=vranges[rangeB], probeAttenuation=1.0)
			repeat = True

		if(rangeA < (len(vranges) - 1) and maxA > 0.95 * vranges[rangeA]):
			rangeA = rangeA + 1
			ps.setChannel(channel="A", coupling="DC",
			              VRange=vranges[rangeA], probeAttenuation=1.0)
			repeat = True

		if(rangeB < (len(vranges) - 1) and maxB > 0.95 * vranges[rangeB]):
			rangeB = rangeB + 1
			ps.setChannel(channel="D", coupling="DC",
			              VRange=vranges[rangeB], probeAttenuation=1.0)
			repeat = True

		gain[i] = aB / aA
		phase[i] = pB - pA

		# , "\toffset:", bB
		print(str(i) + "/" + str(fnum), "\tF:", f, "\tA:",
		      vranges[rangeA], "\tB:", vranges[rangeB], "\tG:", gain[i], "\tP:", phase[i])


ps.close()

fig = plt.figure()
ax = fig.add_subplot(111)

lns1 = ax.loglog(flist, gain, 'xb', label='Amplitude')
#ax2 = ax.twinx()
#lns2 = ax2.semilogx(flist, phase, 'xr', label='Phase')

ax.set_xlabel("f")
ax.set_ylabel("gain")
# ax2.set_ylabel("phase")

#ax2.set_ylim(-2, 2)

# lns = lns1 + lns2
# labs = [l.get_label() for l in lns]
# l = ax.legend(lns, labs, loc='upper left')

plt.show()
