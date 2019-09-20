from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt

def piecewise_linear(x, x0, x1, b, k1, k2, k3):
    condlist = [x < x0, (x >= x0) & (x < x1), x >= x1]
    funclist = [lambda x: k1*x + b, lambda x: k1*x + b + k2*(x-x0), lambda x: k1*x + b + k2*(x-x0) + k3*(x - x1)]
    return np.piecewise(x, condlist, funclist)

def do_piecewise_linear(xx,yy):
  x = np.array(xx)
  y = np.array(yy)
  p , e = optimize.curve_fit(piecewise_linear, x, y)
  xd = np.linspace(min(x), max(x), 1000)
  plt.plot(x, y, "o")
  plt.plot(xd, piecewise_linear(xd, *p))
  plt.show()
