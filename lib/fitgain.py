import numpy as np


def fit(frequency, gain):

	def bandpass(f, gain, cutoffL, orderL, cutoffH, orderH):
		return gain /
		(np.power(np.abs(1 + 1j * f / cutoffL), orderL)
                    * np.power(np.abs(1 + 1j * cutoffH / f), orderH))

	fitresult, _ = scipy.optimize.curve_fit(bandpass, Frequency,
                                         Gain, (10, 10000, 1, 20, 1), bounds=([0, 100, 0.5, 1, 0.5], [100, 1e6, 1000, 1000, 1000]))

	fitresult = np.polyfit(
		np.log10(frequency), np.log10(gain), args.fit_gain_degree)

	Gain_fit = 10**np.polyval(fitresult, np.log10(Frequency_fit))
