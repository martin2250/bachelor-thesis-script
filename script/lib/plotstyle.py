#!/usr/bin/python3
import os

import matplotlib

os.environ['QT_LOGGING_RULES'] = 'qt5ct.debug=false'


def format_bode_plot(axis):
	axis.set_xscale("log", nonposx='clip')
	axis.set_yscale("log", nonposy='clip')
	axis.grid(which='both')
	for subax in [axis.xaxis, axis.yaxis]:
		subax.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%g'))
	axis.set_ylabel('$\\sqrt{J_{ss}^{aus}(f)}$ (µV)')
	axis.set_xlabel('$f$ (Hz)')
	axis.legend()
