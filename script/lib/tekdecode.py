#!/usr/bin/python3
import os
import struct

import numpy as np


def loadFileCSV(filename, channel):
	sample_rate = None
	length = None
	skiprows = 1

	with open(filename) as f:
		for line in f:
			key, *value = line.split(',')
			if key == 'Sample Interval':
				sample_rate = round(1 / float(value[0]))
			elif key == 'Record Length':
				length = round(float(value[0]))
			skiprows += 1
			if key == 'Label':
				break

	_, Y = np.loadtxt(filename, delimiter=',',
                   skiprows=skiprows, unpack=True)

	if len(Y) != length:
		raise UserWarning(
			f'length of {filename} ({len(channels[0])}) does not match description ({length})')

	return Y, sample_rate, length


def loadFileISF(filename, channel):
	with open(filename, 'rb') as f:
		content = f.read()

	hashpos = content.index(b'#')
	head = {key: values for (key, *values) in (line.split(' ')
                                            for line in content[:hashpos].decode().split(';'))}

	digits = int(chr(content[hashpos + 1]), 16)
	data_length = int(content[hashpos + 2: hashpos + 2 + digits].decode())
	data = content[hashpos + 2 + digits:]

	if len(data) != data_length:
		print('length doesn\'t match')
		# raise UserWarning(
		#	f'file length ({len(data)}) does not match stated length ({data_length})')

	length = int(head['NR_PT'][0])
	y_factor = float(head['YMULT'][0])
	y_zero = float(head['YZERO'][0])
	y_offset = float(head['YOFF'][0])
	sample_rate = round(1 / float(head['XINCR'][0]))

	fmt = {'MSB': '>', 'LSB': '<'}[head['BYT_OR'][0]] + str(length) + 'h'

	if int(head['BIT_NR'][0]) == 16:
		Y = np.frombuffer(data, dtype=np.dtype('>i2'))
	elif int(head['BIT_NR'][0]) == 8:
		Y = np.frombuffer(data, dtype=np.dtype('>i2'))
	else:
		raise UserWarning(
			f'ISF file uses incompatible bit depth: {head["BIT_NR"][0]}')

	if len(Y) != length:
		Y = Y[:length]
		print('cropped length')
		# raise UserWarning(
	#		f'data length ({len(Y)}) does not match number of samples ({length})')

	Y = (Y.astype(np.float) - y_offset) * y_factor + y_zero

	return Y, sample_rate, length


matbuffer = {}


def loadFileMAT(filename, channel):
	if filename in matbuffer:
		mat = matbuffer[filename]
	else:
		import scipy.io
		mat = scipy.io.loadmat(filename)
		matbuffer[filename] = mat

	if not channel in mat:
		raise UserWarning(
			f'channel {channel} was not found in file {filename}')

	data = mat[channel][:, 0]
	sample_rate = int(1 / mat['Tinterval'][0, 0])
	return data, sample_rate, len(data)


def loadFile(filename, format=None):
	channel = ''
	if ':' in filename:
		channel, filename = filename.split(':')

	filename = os.path.abspath(filename)
	if format is None:
		format = os.path.splitext(filename)[1]

		if format.startswith('.'):
			format = format[1:]

		if len(format) == 0:
			raise UserWarning(
				f'file type of {filename} could not be determined, use format option')

	parsers = {'csv': loadFileCSV, 'isf': loadFileISF,
            'mat': loadFileMAT, 'html': loadFileISF}

	if not format in parsers:
		raise UserWarning(f'unknown format "{format}"')

	return parsers[format](filename, channel)
