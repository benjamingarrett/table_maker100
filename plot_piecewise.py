from scipy import optimize
import matplotlib.pyplot as plt
import numpy as np
import pwlf

#x = np.array([1, 2, 3,  4,  5,  6,     7,     8,    9,    10,    11,    12,     13,     14,     15], dtype=float)
#y = np.array([5, 7, 9, 11, 13, 15, 28.92, 42.81, 56.7, 70.59, 84.47, 98.36, 112.25, 126.14, 140.03])

#def piecewise_linear(x, x0, y0, k1, k2):
#  return np.piecewise(x, [x < x0, x >= x0], [lambda x:k1*x + y0-k1*x0, lambda x:k2*x + y0-k2*x0])

def do_piecewise_regression(xx,yy,num_pieces=2):
  #for i,xxx in enumerate(xx):
  #  print("do piecewise {} {} {}".format(i,xxx,yy[i]))
  x = np.array(xx, dtype=float)
  y = np.array(yy)
  my_pwlf = pwlf.PiecewiseLinFit(x,y)
  breaks = my_pwlf.fit(num_pieces)
  print('two way breaks {}'.format(breaks))
  x_hat = np.array(breaks)
  #x_hat = np.linspace(x.min(),x.max(),100)
  y_hat = my_pwlf.predict(x_hat)
  return (x_hat,y_hat,breaks)

