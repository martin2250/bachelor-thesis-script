import numpy as np
import scipy.optimize


def fit_hybrid(frequency, gain, print_fit=False):

	def bandpass(f, gain, cutoffL, cutoffH, orderL, orderH, b, c, d, e):
		# subtract mean of cutL/H in log space to get better output for gain
		lf = np.log10(f * np.sqrt(cutoffL / cutoffH))

		# response of first order low and high pass filters
		lowpass = 1 / np.abs(1 + 1j * f / cutoffH)
		highpass = 1 / np.abs(1 + 1j * cutoffL / f)

		# the two functions to model the gain
		# polynomial, centered around the middle of cutL/H in log space
		poly = (1 + b * lf + c * lf**2 + d * lf**3 + e * lf**4)
		# theoretical model with higher order low/high passes
		model = np.power(lowpass, orderH) * np.power(highpass, orderL)

		ratio = (lowpass * highpass)**2

		#output = gain * (np.power(poly, ratio) * np.power(model, (1 - ratio)))
		output = gain * (poly * ratio + model * (1 - ratio))

		return output

	bandfit, _ = scipy.optimize.curve_fit(bandpass, frequency,
                                       gain, (10, 20, 10000, 1, 1, 0, 0, 0, 0), bounds=([0, 5e-1, 5e3, 0.5, 0.5, -1, -1, -1, -1], [500, 5e3, 5e5, 5, 5, 1, 1, 1, 1]))

	if print_fit:
		labels = ['gain', 'cutoffL', 'cutoffH',
                    'orderL', 'orderH', 'b', 'c', 'd', 'e']

		for (label, value) in zip(labels, bandfit):
					print(f'{label}: {value:0.3f}')

	def gain_function(frequency):
		return bandpass(frequency, *bandfit)

	return gain_function


def fit_simple(frequency, gain, print_fit=False):

	def bandpass(f, gain, cutoffL, cutoffH, orderL, orderH):
		return gain / (np.power(np.abs(1 + 1j * f / cutoffH), orderH) * np.power(np.abs(1 + 1j * cutoffL / f), orderL))

	bandfit, _ = scipy.optimize.curve_fit(bandpass, frequency,
                                       gain, (10, 20, 10000, 1, 1), bounds=([0, 5e-1, 5e3, 0.5, 0.5], [500, 5e3, 5e5, 20, 20]))

	if print_fit:
		labels = ['gain', 'cutoffL', 'cutoffH', 'orderL', 'orderH']

		for (label, value) in zip(labels, bandfit):
					print(f'{label}: {value:0.3f}')

	def gain(frequency):
		return bandpass(frequency, *bandfit)

	return gain


fit_lookup = {'hybrid': fit_hybrid, 'simple': fit_simple}
