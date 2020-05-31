# Usage: python analysis.py <folder_w_csv> <n0> <n1> <n2> <type>
# Description: Read all csv files, obtain running max and min, create and check conjectures
#              CSV files have three columns: n, critical cache size, cache misses
#              Of interest here is analysis of critical cache size
#              n0: lowest n for conjecture determination
#              n1: highest n for conjecture determination
#              n2: highest n for conjecture confirmation
#              type: linear or log, default is linear


import csv, os, sys, matplotlib.pyplot as plt
from math import log, sqrt
import numpy as np
from scipy import stats


def update_running_extrema(x, y, mx, mn):
  j = 0
  while j < len(x):
    if x[j] in mx:
      if y[j] > mx[x[j]]:
        mx[x[j]] = y[j]
    elif x[j]-1 in mx:
      mx[x[j]] = mx[x[j]-1]
    else:
      mx[x[j]] = y[j]
    if x[j] in mn:
      if y[j] < mn[x[j]]:
        mn[x[j]] = y[j]
    elif x[j]-1 in mn:
      mn[x[j]] = mn[x[j]-1]
    else:
      mn[x[j]] = y[j]
    j+=1
  return mx, mn


def left_endpoints(pts, n0, n1):
  mx_x, mx_y = [], []
  j = 0
  while j < len(pts):
    if n0 <= pts[j][0] and pts[j][0] <= n1:
      if pts[j][1] > pts[j-1][1]:
        mx_x.append(pts[j][0])
        mx_y.append(pts[j][1])
    j += 1
  return mx_x, mx_y


def get_list(fn):
  return [ln.rstrip('\n').split(',') for ln in open(fn)]


def get_points(d):
  x, y = [], []
  for k, v in d.items():
    x.append(k)
    y.append(v)
  return x, y


def loglog_regression(x, y, basex=2, basey=2):
  lgx = [log(k, basex) for k in x]
  lgy = [log(k, basey) for k in y]
  m, b, r, p, err = stats.linregress(lgx, lgy)
  return m, b


def find_bound_m(x, y, n0, n1, eps=0.0001):
  m, b = loglog_regression(x, y)
  success = False
  bound = lambda x: (2**b) * (x**m)
  while not success:
    j = 0
    m += eps
    while j < len(x) and n0 <= x[j] and x[j] <= n1:
      if y[j] > bound(x[j]):
        success = False
        break
      else:
        success = True
      j += 1
  return m, b


def find_bound_b(x, y, n0, n1, eps=0.0001):
  m, b = loglog_regression(x, y)
  success = False
  bound = lambda x: (2**b) * (x**m)
  while not success:
    j = 0
    b += eps
    while j < len(x) and n0 <= x[j] and x[j] <= n1:
      if y[j] > bound(x[j]):
        success = False
        break
      else:
        success = True
      j += 1
  return m, b


def confirm_upper_bound(x, y, f, n0, n2):
  c = 0
  for j in range(len(x)):
    if n0 <= x[j] and x[j] <= n2:
      if f(x[j]) < y[j]:
        c += 1
  return c


def conjecture_points(x, f):
  y = [f(k) for k in x]
  return x, y


print('{}'.format(sys.argv))
if len(sys.argv) >= 6:
  if str(sys.argv[5]).casefold()=='log'.casefold():
    scale = 'log'
  else:
    scale = 'linear'
else:
  scale = 'linear'
fig = plt.figure()
ax = fig.add_subplot(111)
col = 1
files = [f for f in os.listdir(sys.argv[1]) if 'csv' in f]
rmx, rmn = {}, {}
k = 0
max_x = 0
while k < len(files):
  lst = get_list(sys.argv[1]+'/'+files[k])
  j = 1
  x = []
  y = []
  while j < len(lst):
    x.append(int(lst[j][0]))
    y.append(int(lst[j][col]))
    max_x = int(lst[j][0]) if int(lst[j][0]) > max_x else max_x
    j += 1
  rmx, rmn = update_running_extrema(x, y, rmx, rmn)
  if False:
    if scale=='linear':
      ax.plot(x, y)
    else:
      ax.loglog(x, y, basex=2, basey=2)
  k += 1

if len(sys.argv) >= 3:
  n0 = int(sys.argv[2])
else:
  n0 = 0
if len(sys.argv) >= 4:
  n1 = int(sys.argv[3])
else:
  n1 = max_x
if len(sys.argv) >= 5:
  n2 = int(sys.argv[4])
else:
  n2 = max_x

pts = [(k, rmx[k]) for k in sorted(rmx.keys())]

rmx_x = [k[0] for k in pts]
rmx_y = [k[1] for k in pts]

lft_x, lft_y = left_endpoints(pts, n0, n1)

x, y = get_points(rmx)

m_best, b = find_bound_m(lft_x, lft_y, n0, n1)
m, b_best = find_bound_b(lft_x, lft_y, n0, n1)
bound1 = lambda x: 2**b * x**m_best
bound2 = lambda x: 2**b_best * x**m
bound3 = lambda x: 2**b_best * x**m_best
cj1_x, cj1_y = conjecture_points(rmx.keys(), bound1)
cj2_x, cj2_y = conjecture_points(rmx.keys(), bound2)
cj3_x, cj3_y = conjecture_points(rmx.keys(), bound3)

errors1 = confirm_upper_bound(rmx_x, rmx_y, bound1, n0, n2)
errors2 = confirm_upper_bound(rmx_x, rmx_y, bound2, n0, n2)
errors3 = confirm_upper_bound(rmx_x, rmx_y, bound3, n0, n2)

print('conjecture 1: {} {}  errors {}'.format(2**b, m_best, errors1))
print('conjecture 2: {} {}  errors {}'.format(2**b_best, m, errors2))
print('conjecture 3: {} {}  errors {}'.format(2**b_best, m_best, errors3))

if scale=='linear':
  ax.plot(lft_x, lft_y, 'o', label='left endpoints')
  ax.plot(x, y, label='running max')
  #ax.plot(cj1_x, cj1_y, '*', label='conjecture 1')
  ax.plot(cj2_x, cj2_y, '*', label='conjecture: {}*n^{}, confirmation errors: {}'.format(2**b_best, m, errors2))
  #ax.plot(cj3_x, cj3_y, '*', label='conjecture 3')

else:
  ax.loglog(lft_x, lft_y, 'o', label='left endpoints', basex=2, basey=2)
  ax.loglog(x, y, label='running max', basex=2, basey=2)
  #ax.loglog(cj1_x, cj1_y, '*', label='conjecture 1', basex=2, basey=2)
  ax.loglog(cj2_x, cj2_y, '*', label='conjecture: {}*n^{}, confirmation errors: {}'.format(2**b_best, m, errors2), basex=2, basey=2)
  #ax.loglog(cj3_x, cj3_y, '*', label='conjecture 3', basex=2, basey=2)

plt.xlabel('problem size (n)')
plt.ylabel('critical cache size')
ax.legend(loc='upper left')
t = 'OLCS v4 traceback, LRU, critical cache size'
t+= '\nInstance type: 0^a 1^a ... b^a (b+1)^(a mod n), where a=floor(n^c), b=floor(n/a)'
t+= '\nfor all c in the range (0,1) in increments of 0.01'
t+= '\nConjecture based on n between {} and {}'.format(n0, n1)
plt.title(t)
plt.show()
