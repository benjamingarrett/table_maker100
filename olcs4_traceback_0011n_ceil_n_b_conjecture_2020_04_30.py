# Usage: <folder> <b> <min_x> <max_x> <confirm_to_x>
# n,csize,misses
# Trying polynomial regression here
# Copied from olcs4_traceback_0011n_ceil_n_b_conjecture_2020_04_22.py


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


def get_best_poly_fit(pts, n0, n1):
  cjpts = [(k[0], k[1]) for k in pts if n0 <= k[0] and k[0] <= n1]
  x = [k[0] for k in cjpts]
  y = [k[1] for k in cjpts]
  p = np.poly1d(np.polyfit(x, y, 2))
  r2 = r2_score(y, p(x))
  return p, r2


def get_poly_fit_pts(poly, n0, n1):
  x = np.linspace(n0, n1, 100)
  y = poly(x)
  pts = []
  j = 0
  while j < len(x):
    pts.append((x[j], y[j]))
    j += 1
  return pts


def get_poly_pts(c2, c1, c0, n0, n1):
  x = np.linspace(n0, n1, 100)
  f = lambda x: c2 * x**2 + c1 * x + c0
  y = f(x)
  pts = []
  j = 0
  while j < len(x):
    pts.append((x[j], y[j]))
    j += 1
  return pts


def get_poly_fit_str(poly):
  s = ''
  j = 0
  while j < poly.o:
    exp = ' x'
    if poly.o - j > 1:
      exp += '^{}'.format(poly.o - j)
    if poly.c[j+1] >= 0:
      s += '{} {} +'.format(poly.c[j], exp)
    else:
      s += '{} {} '.format(poly.c[j], exp)
    j += 1
  s += '{}'.format(poly.c[poly.o])
  return s


def get_poly_str(poly_bound_c2, poly_bound_c1, poly_bound_c0):
  s = '{} x^2 '.format(poly_bound_c2)
  if poly_bound_c1 >= 0:
    s += '+{} x '.format(poly_bound_c1)
  else:
    s += '{} x '.format(poly_bound_c1)
  if poly_bound_c0 >= 0:
    s += '+{}'.format(poly_bound_c0)
  else:
    s += '{}'.format(poly_bound_c0)
  return s


def get_best_poly_bound_0(pts, n0, n1, eps=0.0001):
  cjpts = [(k[0], k[1]) for k in pts if n0 <= k[0] and k[0] <= n1]
  x = [k[0] for k in cjpts]
  y = [k[1] for k in cjpts]
  p = np.poly1d(np.polyfit(x, y, 2))
  r2 = r2_score(y, p(x))
  cnt = 0
  c2 = p.c[0]
  c1 = p.c[1]
  c0 = p.c[2]
  bound = lambda x: c2 * x**2 + c1 * x + c0
  while not bounds_above(cjpts, bound):
    c0 += eps
    cnt += 1
    if cnt > 50000:
      print('exiting before convergence')
      exit()
  return c2, c1, c0


def get_best_poly_bound_1(pts, n0, n1, eps=0.0001):
  cjpts = [(k[0], k[1]) for k in pts if n0 <= k[0] and k[0] <= n1]
  x = [k[0] for k in cjpts]
  y = [k[1] for k in cjpts]
  p = np.poly1d(np.polyfit(x, y, 2))
  r2 = r2_score(y, p(x))
  cnt = 0
  c2 = p.c[0]
  c1 = p.c[1]
  c0 = p.c[2]
  bound = lambda x: c2 * x**2 + c1 * x + c0
  while not bounds_above(cjpts, bound):
    c1 += eps
    cnt += 1
    if cnt > 50000:
      print('exiting before convergence')
      exit()
  return c2, c1, c0


def get_best_poly_bound_2(pts, n0, n1, eps=0.0001):
  cjpts = [(k[0], k[1]) for k in pts if n0 <= k[0] and k[0] <= n1]
  x = [k[0] for k in cjpts]
  y = [k[1] for k in cjpts]
  p = np.poly1d(np.polyfit(x, y, 2))
  r2 = r2_score(y, p(x))
  cnt = 0
  c2 = p.c[0]
  c1 = p.c[1]
  c0 = p.c[2]
  bound = lambda x: c2 * x**2 + c1 * x + c0
  while not bounds_above(cjpts, bound):
    c2 += eps
    cnt += 1
    if cnt > 50000:
      print('exiting before convergence')
      exit()
  return c2, c1, c0


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






if len(sys.argv) < 6:
  print('Usage: <folder> <chosen_b> <min_x> <max_x> <confirm_to_x>')
  exit()
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
confirm_x = [k[0] for k in confirm_pts]
confirm_y = [k[1] for k in confirm_pts]

poly_lft_obj, r2_lft = get_best_poly_fit(lft, min_x, max_x)
poly_rgh_obj, r2_rgh = get_best_poly_fit(rgh, min_x, max_x)
poly_lft_pts = get_poly_fit_pts(poly_lft_obj, min_x, confirm_to_x)
poly_rgh_pts = get_poly_fit_pts(poly_rgh_obj, min_x, confirm_to_x)
poly_lft_str = get_poly_fit_str(poly_lft_obj)
poly_rgh_str = get_poly_fit_str(poly_rgh_obj)

eps = 0.001
poly_bound_c2, poly_bound_c1, poly_bound_c0 = get_best_poly_bound_0(lft, min_x, max_x, eps)
poly_bound_pts = get_poly_pts(poly_bound_c2, poly_bound_c1, poly_bound_c0, min_x, confirm_to_x)
poly_bound_str = get_poly_str(poly_bound_c2, poly_bound_c1, poly_bound_c0)
poly_bound = lambda x: poly_bound_c2 * x**2 + poly_bound_c1 * x + poly_bound_c0
poly_bound_confirmed = bounds_above(confirm_pts, poly_bound)
if poly_bound_confirmed == False:
  poly_bound_c2, poly_bound_c1, poly_bound_c0 = get_best_poly_bound_1(lft, min_x, max_x, eps)
  poly_bound_pts = get_poly_pts(poly_bound_c2, poly_bound_c1, poly_bound_c0, min_x, confirm_to_x)
  poly_bound_str = get_poly_str(poly_bound_c2, poly_bound_c1, poly_bound_c0)
  poly_bound = lambda x: poly_bound_c2 * x**2 + poly_bound_c1 * x + poly_bound_c0
  poly_bound_confirmed = bounds_above(confirm_pts, poly_bound) 
if poly_bound_confirmed == False:
  poly_bound_c2, poly_bound_c1, poly_bound_c0 = get_best_poly_bound_2(lft, min_x, max_x, eps)
  poly_bound_pts = get_poly_pts(poly_bound_c2, poly_bound_c1, poly_bound_c0, min_x, confirm_to_x)
  poly_bound_str = get_poly_str(poly_bound_c2, poly_bound_c1, poly_bound_c0)
  poly_bound = lambda x: poly_bound_c2 * x**2 + poly_bound_c1 * x + poly_bound_c0
  poly_bound_confirmed = bounds_above(confirm_pts, poly_bound)


poly_lft_confirm_r2 = r2_score(confirm_y, poly_lft_obj(confirm_x))
poly_rgh_confirm_r2 = r2_score(confirm_y, poly_rgh_obj(confirm_x))


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
ax.plot([k[0] for k in rmx], [k[1] for k in rmx], '*', label='running max of critical cache size for b = 3')
#ax.plot([k[0] for k in poly_lft_pts], [k[1] for k in poly_lft_pts], label='left endpoint poly fit: {}, r^2: {}'.format(poly_lft_str, poly_lft_confirm_r2))
#ax.plot([k[0] for k in poly_rgh_pts], [k[1] for k in poly_rgh_pts], label='right endpoint poly fit: {}, r^2: {}'.format(poly_rgh_str, poly_rgh_confirm_r2))
if poly_bound_confirmed:
  ax.plot([k[0] for k in poly_bound_pts], [k[1] for k in poly_bound_pts], label='upper bound: {}'.format(poly_bound_str))

#ax.loglog([k[0] for k in rmx], [k[1] for k in rmx], '*', label='running max of critical cache size for b = 3', basex=2, basey=2)

#ax.loglog([k[0] for k in lft], [k[1] for k in lft], '*', label='left endpoints running max of critical cache size for b = 3', basex=2, basey=2)
#ax.loglog([k[0] for k in rgh], [k[1] for k in rgh], '*', label='right endpoints running max of critical cache size for b = 3', basex=2, basey=2)


#if upper_confirmed1 and best_j_lft==0:
#  ax.loglog([k[0] for k in cj1_up], [k[1] for k in cj1_up], label='conjecture, {}'.format(upper_conj_str1), basex=2, basey=2)
#if upper_confirmed2 and best_j_lft==1:
#  ax.loglog([k[0] for k in cj2_up], [k[1] for k in cj2_up], label='conjecture, {}'.format(upper_conj_str2), basex=2, basey=2)
#if upper_confirmed3 and best_j_lft==2:
#  ax.loglog([k[0] for k in cj3_up], [k[1] for k in cj3_up], label='conjecture, {}'.format(upper_conj_str3), basex=2, basey=2)

#if lower_confirmed1 and best_j_rgh==0:
#  ax.loglog([k[0] for k in cj1_lo], [k[1] for k in cj1_lo], label='conjecture, {}'.format(lower_conj_str1), basex=2, basey=2)
#if lower_confirmed2 and best_j_rgh==1:
#  ax.loglog([k[0] for k in cj2_lo], [k[1] for k in cj2_lo], label='conjecture, {}'.format(lower_conj_str2), basex=2, basey=2)
#if lower_confirmed3 and best_j_rgh==2:
#  ax.loglog([k[0] for k in cj3_lo], [k[1] for k in cj3_lo], label='conjecture, {}'.format(lower_conj_str3), basex=2, basey=2)

plt.xlabel('problem size (n)')
plt.ylabel('critical cache size')
t = 'OLCS v4 traceback, LRU, critical cache size (csize)'
t+= '\nInstance type: a = ceiling(n/b)'
t+= '\n1st sequence: 0^a 1^a ... (b-1)^(n-(b-1)a)'
t+= '\n2nd sequence: (b-1)^(n-(b-1)a) ... 1^a 0^a'
ax.legend(loc='upper left')
plt.title(t)
plt.show()
