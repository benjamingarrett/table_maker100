# Usage: <folder> <b> <min_x> <max_x> <confirm_to_x>
# n,csize,misses


import csv, os, sys, matplotlib.pyplot as plt
from math import log, sqrt, floor
import numpy as np
from scipy import stats
from sklearn.metrics import r2_score


def get_list(fn):
  return [ln.rstrip('\n').split(',') for ln in open(fn)]


def points_dict(files, col):
  k = 0
  d = {}
  while k < len(files):
    tmp_str = files[k][15:]
    b = int(tmp_str[0:tmp_str.find('.')])
    d[b] = []
    lst = get_list(sys.argv[1]+'/'+files[k])
    j = 1   # skip heading
    while j < len(lst):
      d[b].append((int(lst[j][0]), int(lst[j][col])))
      j += 1
    k += 1
  return d


def loglog_regression(x, y, basex=2, basey=2):
  lgx = [log(k, basex) for k in x]
  lgy = [log(k, basey) for k in y]
  m, b, r, p, err = stats.linregress(lgx, lgy)
  return m, b


def running_max(pts):
  j = 1
  lst = [(pts[0][0], pts[0][1])]
  while j < len(pts):
    if pts[j][1] > lst[j-1][1]:
      lst.append((pts[j][0], pts[j][1]))
    else:
      lst.append((pts[j][0], lst[j-1][1]))
    j += 1
  return lst


def left_endpoints(pts):
  lst = [(pts[0][0], pts[0][1])]
  j = 1
  while j < len(pts):
    if pts[j][1] > pts[j-1][1]:
      lst.append((pts[j][0], pts[j][1]))
    j += 1
  return lst


def right_endpoints(pts):
  lst = [(pts[0][0], pts[0][1])]
  j = 1
  while j < len(pts):
    if pts[j][1] > pts[j-1][1]:
      lst.append((pts[j-1][0], pts[j-1][1]))
    j += 1
  return lst


def get_best_fit(pts, n0, n1):
  cjpts = [(k[0], k[1]) for k in pts if n0 <= k[0] and k[0] <= n1]
  cx = [k[0] for k in cjpts]
  cy = [k[1] for k in cjpts]
  m, b = loglog_regression(cx, cy)
  return m, b


def find_upper_bound_m(pts, n0, n1, eps=0.0001):
  x = [k[0] for k in pts]
  y = [k[1] for k in pts]
  cjpts = [(k[0], k[1]) for k in pts if n0 <= k[0] and k[0] <= n1]
  cx = [k[0] for k in cjpts]
  cy = [k[1] for k in cjpts]
  m, b = loglog_regression(cx, cy)
  upper_bound = lambda x: (2**b) * (x**m)
  cnt = 0
  while not bounds_above(cjpts, upper_bound):
    m += eps
    cnt += 1
    if cnt > 20000:
      print('exiting before convergence')
      exit()
  return m, b


def find_lower_bound_m(pts, n0, n1, eps=0.0001):
  x = [k[0] for k in pts]
  y = [k[1] for k in pts]
  cjpts = [(k[0], k[1]) for k in pts if n0 <= k[0] and k[0] <= n1]
  cx = [k[0] for k in cjpts]
  cy = [k[1] for k in cjpts]
  m, b = loglog_regression(cx, cy)
  lower_bound = lambda x: (2**b) * (x**m)
  cnt = 0
  while not bounds_below(cjpts, lower_bound):
    m -= eps
    cnt += 1
    if cnt > 200000:
      print('exiting before convergence')
      exit()
  return m, b


def find_upper_bound_b(pts, n0, n1, eps=0.0001):
  x = [k[0] for k in pts]
  y = [k[1] for k in pts]
  cjpts = [(k[0], k[1]) for k in pts if n0 <= k[0] and k[0] <= n1]
  cx = [k[0] for k in cjpts]
  cy = [k[1] for k in cjpts]
  m, b = loglog_regression(cx, cy)
  upper_bound = lambda x: (2**b) * (x**m)
  cnt = 0
  while not bounds_above(cjpts, upper_bound):
    b += eps
    cnt += 1
    if cnt > 20000:
      print('exiting before convergence')
      exit()
  return m, b


def find_lower_bound_b(pts, n0, n1, eps=0.0001):
  x = [k[0] for k in pts]
  y = [k[1] for k in pts]
  cjpts = [(k[0], k[1]) for k in pts if n0 <= k[0] and k[0] <= n1]
  cx = [k[0] for k in cjpts]
  cy = [k[1] for k in cjpts]
  m, b = loglog_regression(cx, cy)
  lower_bound = lambda x: (2**b) * (x**m)
  cnt = 0
  while not bounds_below(cjpts, lower_bound):
    b -= eps
    cnt += 1
    if cnt > 200000:
      print('exiting before convergence')
      exit()
  return m, b


def find_upper_bound_m_and_b(pts, n0, n1, eps=0.0001):
  x = [k[0] for k in pts]
  y = [k[1] for k in pts]
  cjpts = [(k[0], k[1]) for k in pts if n0 <= k[0] and k[0] <= n1]
  cx = [k[0] for k in cjpts]
  cy = [k[1] for k in cjpts]
  m, b = loglog_regression(cx, cy)
  m1, m2 = m, m
  b1, b2 = b, b
  upper_bound1 = lambda x: (2**b1) * (x**m1)
  upper_bound2 = lambda x: (2**b2) * (x**m2)
  cnt = 0
  while not bounds_above(cjpts, upper_bound1):
    m1 += eps
    cnt += 1
    if cnt > 20000:
      print('exiting before convergence')
      exit()
  cnt = 0
  while not bounds_above(cjpts, upper_bound2):
    b2 += eps
    cnt += 1
    if cnt > 20000:
      print('exiting before convergence')
      exit()
  return m1, b2


def find_lower_bound_m_and_b(pts, n0, n1, eps=0.0001):
  x = [k[0] for k in pts]
  y = [k[1] for k in pts]
  cjpts = [(k[0], k[1]) for k in pts if n0 <= k[0] and k[0] <= n1]
  cx = [k[0] for k in cjpts]
  cy = [k[1] for k in cjpts]
  m, b = loglog_regression(cx, cy)
  m1, m2 = m, m
  b1, b2 = b, b
  lower_bound1 = lambda x: (2**b1) * (x**m1)
  lower_bound2 = lambda x: (2**b2) * (x**m2)
  cnt = 0
  while not bounds_below(cjpts, lower_bound1):
    m1 -= eps
    cnt -= 1
    if cnt > 200000:
      print('exiting before convergence')
      exit()
  cnt = 0
  while not bounds_below(cjpts, lower_bound2):
    b2 -= eps
    cnt += 1
    if cnt > 200000:
      print('exiting before convergence')
      exit()
  return m1, b2


def conjecture_points(min_x, max_x, f):
  return [(k, f(k)) for k in range(min_x, max_x+1)]


def bounds_above(pts, f):
  j = 0
  while j < len(pts):
    if float(pts[j][1]) >= f(pts[j][0]):
      return False
    j += 1
  return True


def bounds_below(pts, f):
  j = 0
  while j < len(pts):
    if float(pts[j][1]) <= f(pts[j][0]):
      return False
    j += 1
  return True


files = [f for f in os.listdir(sys.argv[1]) if 'csv' in f]
chosen_b = int(sys.argv[2])
min_x = int(sys.argv[3])
max_x = int(sys.argv[4])
confirm_to_x = int(sys.argv[5])
d = points_dict(files, 1)
pts = [(k[0], k[1]) for k in sorted(d[chosen_b], key=lambda x: x[0])]
rmx = running_max(pts)
lft = left_endpoints(rmx)
rgh = right_endpoints(rmx)
confirm_pts = [(k[0], k[1]) for k in rmx if min_x <= k[0] and k[0] <= confirm_to_x]

m_best_fit_lft, b_best_fit_lft = get_best_fit(lft, min_x, max_x)
m_best_fit_rgh, b_best_fit_rgh = get_best_fit(rgh, min_x, max_x)
confirmed_lft = []
confirmed_rgh = []

m1_up, b1_up = find_upper_bound_m(lft, min_x, max_x)
upper_bound1 = lambda x: (2**b1_up) * (x**m1_up)
cj1_up = conjecture_points(min_x, confirm_to_x, upper_bound1)
upper_confirmed1 = bounds_above(confirm_pts, upper_bound1)
upper_conj_str1 = 'max(csize(n)) <= {} * n^{}, n >= {}'.format(2**b1_up, m1_up, min_x)
if upper_confirmed1:
  confirmed_lft.append((m1_up, b1_up))


m1_lo, b1_lo = find_lower_bound_m(rgh, min_x, max_x)
lower_bound1 = lambda x: (2**b1_lo) * (x**m1_lo)
cj1_lo = conjecture_points(min_x, confirm_to_x, lower_bound1)
lower_confirmed1 = bounds_below(confirm_pts, lower_bound1)
lower_conj_str1 = 'max(csize(n)) >= {} * n^{}, n >= {}'.format(2**b1_lo, m1_lo, min_x)
if lower_confirmed1:
  confirmed_rgh.append((m1_lo, b1_lo))


m2_up, b2_up = find_upper_bound_b(lft, min_x, max_x)
upper_bound2 = lambda x: (2**b2_up) * (x**m2_up)
cj2_up = conjecture_points(min_x, confirm_to_x, upper_bound2)
upper_confirmed2 = bounds_above(confirm_pts, upper_bound2)
upper_conj_str2 = 'max(csize(n)) <= {} * n^{}, n >= {}'.format(2**b2_up, m2_up, min_x)
if upper_confirmed2:
  confirmed_lft.append((m2_up, b2_up))


m2_lo, b2_lo = find_lower_bound_b(rgh, min_x, max_x)
lower_bound2 = lambda x: (2**b2_lo) * (x**m2_lo)
cj2_lo = conjecture_points(min_x, confirm_to_x, lower_bound2)
lower_confirmed2 = bounds_below(confirm_pts, lower_bound2)
lower_conj_str2 = 'max(csize(n)) >= {} * n^{}, n >= {}'.format(2**b2_lo, m2_lo, min_x)
if lower_confirmed2:
  confirmed_rgh.append((m2_lo, b2_lo))


m3_up, b3_up = find_upper_bound_m_and_b(lft, min_x, max_x)
upper_bound3 = lambda x: (2**b3_up) * (x**m3_up)
cj3_up = conjecture_points(min_x, confirm_to_x, upper_bound3)
upper_confirmed3 = bounds_above(confirm_pts, upper_bound3)
upper_conj_str3 = 'max(csize(n)) <= {} * n^{}, n >= {}'.format(2**b3_up, m3_up, min_x)
if upper_confirmed3:
  confirmed_lft.append((m3_up, b3_up))


m3_lo, b3_lo = find_lower_bound_m_and_b(rgh, min_x, max_x)
lower_bound3 = lambda x: (2**b3_lo) * (x**m3_lo)
cj3_lo = conjecture_points(min_x, confirm_to_x, lower_bound3)
lower_confirmed3 = bounds_below(confirm_pts, lower_bound3)
lower_conj_str3 = 'max(csize(n)) >= {} * n^{}, n >= {}'.format(2**b3_lo, m3_lo, min_x)
if lower_confirmed3:
  confirmed_rgh.append((m3_lo, b3_lo))


if len(confirmed_lft) > 0:
  best_diff = abs(m_best_fit_lft - confirmed_lft[0][0])
  best_m_lft = confirmed_lft[0][0]
  best_j_lft = 0
  if len(confirmed_lft) > 1:
    j = 1
    while j < len(confirmed_lft):
      if abs(m_best_fit_lft - confirmed_lft[j][0]) < best_diff:
        best_diff = abs(m_best_fit_lft - confirmed_lft[j][0])
        best_m_lft = confirmed_lft[j][0]
        best_j_lft = j
      j += 1
else:
  best_j_lft = -1
if len(confirmed_rgh) > 0:
  best_diff = abs(m_best_fit_rgh - confirmed_rgh[0][0])
  best_m_rgh = confirmed_rgh[0][0]
  best_j_rgh = 0
  if len(confirmed_rgh) > 1:
    j = 1
    while j < len(confirmed_rgh):
      if abs(m_best_fit_rgh - confirmed_rgh[j][0]) < best_diff:
        best_diff = abs(m_best_fit_rgh - confirmed_rgh[j][0])
        best_m_rgh = confirmed_rgh[j][0]
        best_j_rgh = j
      j += 1
else:
  best_j_rgh = -1


fig = plt.figure()
ax = fig.add_subplot(111)
ax.loglog([k[0] for k in rmx], [k[1] for k in rmx], '*', label='running max of critical cache size for b = 3', basex=2, basey=2)

#ax.loglog([k[0] for k in lft], [k[1] for k in lft], '*', label='left endpoints running max of critical cache size for b = 3', basex=2, basey=2)
#ax.loglog([k[0] for k in rgh], [k[1] for k in rgh], '*', label='right endpoints running max of critical cache size for b = 3', basex=2, basey=2)


if upper_confirmed1 and best_j_lft==0:
  ax.loglog([k[0] for k in cj1_up], 
            [k[1] for k in cj1_up], 
            label='log-log regresssion of left endpoints, {}, r^2: {}'.format(upper_conj_str1, r2_score([k[1] for k in confirm_pts], [k[1] for k in cj1_up])), basex=2, basey=2)
if upper_confirmed2 and best_j_lft==1:
  ax.loglog([k[0] for k in cj2_up], 
            [k[1] for k in cj2_up], 
            label='log-log regresssion of left endpoints, {}, r^2: {}'.format(upper_conj_str2, r2_score([k[1] for k in confirm_pts], [k[1] for k in cj2_up])), basex=2, basey=2)
if upper_confirmed3 and best_j_lft==2:
  ax.loglog([k[0] for k in cj3_up], 
            [k[1] for k in cj3_up], 
            label='log-log regresssion of left endpoints, {}, r^2: {}'.format(upper_conj_str3, r2_score([k[1] for k in confirm_pts], [k[1] for k in cj3_up])), basex=2, basey=2)

if lower_confirmed1 and best_j_rgh==0:
  ax.loglog([k[0] for k in cj1_lo], 
            [k[1] for k in cj1_lo], 
            label='log-log regresssion of right endpoints, {}, r^2: {}'.format(lower_conj_str1, r2_score([k[1] for k in confirm_pts], [k[1] for k in cj1_lo])), basex=2, basey=2)
if lower_confirmed2 and best_j_rgh==1:
  ax.loglog([k[0] for k in cj2_lo], 
            [k[1] for k in cj2_lo], 
            label='log-log regresssion of right endpoints, {}, r^2: {}'.format(lower_conj_str2, r2_score([k[1] for k in confirm_pts], [k[1] for k in cj2_lo])), basex=2, basey=2)
if lower_confirmed3 and best_j_rgh==2:
  ax.loglog([k[0] for k in cj3_lo], 
            [k[1] for k in cj3_lo], 
            label='log-log regresssion of right endpoints, {}, r^2: {}'.format(lower_conj_str3, r2_score([k[1] for k in confirm_pts], [k[1] for k in cj3_lo])), basex=2, basey=2)

plt.xlabel('problem size (n)')
plt.ylabel('critical cache size')
t = 'OLCS v4 traceback, LRU, critical cache size (csize)'
t+= '\nInstance type: a = ceiling(n/b)'
t+= '\n1st sequence: 0^a 1^a ... (b-1)^(n-(b-1)a)'
t+= '\n2nd sequence: (b-1)^(n-(b-1)a) ... 1^a 0^a'
ax.legend(loc='upper left')
plt.title(t)
plt.show()
