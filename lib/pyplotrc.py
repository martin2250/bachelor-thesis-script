import matplotlib

# prevent x axis label being cut off
matplotlib.rcParams['figure.autolayout'] = True
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['pgf.rcfonts'] = True
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['pgf.preamble'] = matplotlib.rcParams['text.latex.preamble'] = [
    r'\usepackage{amsmath}',
    r'\usepackage{amssymb}',
    r'\usepackage{siunitx}'
]
matplotlib.use('pgf')
