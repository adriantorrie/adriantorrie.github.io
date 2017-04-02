# coding: utf-8

# Python version
import sys
print('Python: {}\n'.format(sys.version))

# matplotlib
import matplotlib
print('matplotlib:\t{}'.format(matplotlib.__version__))

# numpy
import numpy
print('numpy:\t\t{}'.format(numpy.__version__))

# pandas
import pandas
print('pandas:\t\t{}'.format(pandas.__version__))

# quandl
import quandl
print('quandl:\t\t{}'.format(quandl.version.VERSION))

# scikit-learn
import sklearn
print('sklearn:\t{}'.format(sklearn.__version__))

# scipy
import scipy
print('scipy:\t\t{}'.format(scipy.__version__))

# statsmodels
import statsmodels
print('statsmodels:\t{}'.format(statsmodels.__version__))

# tensorflow
import tensorflow
print('tensorflow:\t{}'.format(tensorflow.__version__))
