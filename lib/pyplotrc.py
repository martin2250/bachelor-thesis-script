import matplotlib

matplotlib.rcParams['figure.autolayout'] = True
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['pgf.preamble'] = matplotlib.rcParams['text.latex.preamble'] = [
	r'\usepackage{amsmath}',
	r'\usepackage{amssymb}',
	r'\usepackage{siunitx}'
]
