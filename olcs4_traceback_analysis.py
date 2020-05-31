# Usage: python lcs_analysis.py <csv_file> <# of col to analyze (0-based)> <has_heading> <lowest n> <highest n> <confirmation max>
# has_heading: 1 for true, 0 for false, if true skips first line
# Expects a 3-column csv file
# Typically column 0 is n
#                  1 is cache size
#                  2 is cache misses


import csv,os,sys,matplotlib as plt
from math import log,sqrt
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


def running_max(data,n0,n2,col):
  running_max_x = [data[n0][0]]
  running_max_y = [data[n0][col]]
  j = n0
  while j < len(data):
    if j <= n2:
      running_max_x.append(data[j][0])
      if data[j][col] > running_max_y[-1]:
        running_max_y.append(data[j][col])
      else:
        running_max_y.append(running_max_y[-1])
    else:
      break
    j+=1
  return running_max_x, running_max_y


def left_endpoints(x,y,n1):
  mx_x=[]
  mx_y=[]
  j=0
  while j < len(x):
    if x[j] <= n1:
      if y[j] > y[j-1]:
        mx_x.append(x[j])
        mx_y.append(y[j])
    else:
      break
    j+=1
  return mx_x, mx_y


def right_endpoints(x,y,n1):
  mn_x=[]
  mn_y=[]
  j=0
  while j < len(x):
    if x[j] <= n1:
      if y[j] > y[j-1]:
        mn_x.append(x[j-1])
        mn_y.append(y[j-1])
    else: 
      break
    j+=1
  return mn_x, mn_y


def semilogx_regression(x, y, basex=2):
  lgx = [log(k, basex) for k in x]
  m, b, r, p, err = stats.linregress(lgx, y)
  return m, b


def loglog_regression(x, y, basex=2, basey=2):
  lgx = [log(k, basex) for k in x]
  lgy = [log(k, basey) for k in y]
  m, b, r, p, err = stats.linregress(lgx, lgy)
  return m, b


def conjecture_points(x,f):
  y = [f(k) for k in x]
  return x,y


def find_bound(mx_x, mx_y, min_x=0, max_x=0, eps=0.0001):
  m_upper, b_upper = loglog_regression(mx_x, mx_y)
  m_upper_best = m_upper
  b_upper_best = 2**b_upper
  if min_x == 0:
    smallest_x = min(mx_x)
  else:
    smallest_x = min_x
  if max_x == 0:
    biggest_x = max(mx_x)
  else:
    biggest_x = max_x
  bound = lambda x: (b_upper_best) * (x**m_upper_best)
  if True:
    success = False
    while not success:
      j = 0
      b_upper_best += eps
      while smallest_x <= mx_x[j] and mx_x[j] <= biggest_x:
        if mx_y[j] > bound(mx_x[j]):
          success = False
          break
        else:
          success = True
        j += 1
  if True:
    bound = lambda x: (2**b_upper) * (x**m_upper_best)
    success = False
    while not success:
      j = 0
      m_upper_best += eps
      while smallest_x <= mx_x[j] and mx_x[j] <= biggest_x:
        if mx_y[j] > bound(mx_x[j]):
          success = False
          break
        else:
          success = True
        j += 1
  return m_upper_best, b_upper_best


def confirm_upper_bound(data_x, data_y, bounding_function, min_x=0, max_x=0):
  if min_x == 0:
    smallest_x = min(mx_x)
  else:
    smallest_x = min_x
  if max_x == 0:
    biggest_x = max(mx_x)
  else:
    biggest_x = max_x
  errors = 0
  j = 0
  while j < len(data_x):
    if smallest_x <= data_x[j] and data_x[j] <= biggest_x:
      if data_y[j] > bounding_function(data_x[j]):
        errors += 1
    j += 1
  return errors


def confirm_lower_bound(data_x, data_y, bounding_function, min_x=0, max_x=0):
  if min_x == 0:
    smallest_x = min(mx_x)
  else:
    smallest_x = min_x
  if max_x == 0:
    biggest_x = max(mx_x)
  else:
    biggest_x = max_x
  errors = 0
  j = 0
  while j < len(data_x):
    if smallest_x <= data_x[j] and data_x[j] <= biggest_x:
      if data_y[j] < bounding_function(data_x[j]):
        errors += 1
    j += 1
  return errors


print('{}'.format(sys.argv))
lines=[x for x in [ln.rstrip('\n').split(',') for ln in open(sys.argv[1])]]
if sys.argv[3].casefold()=='1'.casefold():
  lists=[(int(x[0]),int(x[1]),int(x[2])) for x in lines[1:]]
else:
  lists=[(int(x[0]),int(x[1]),int(x[2])) for x in lines]
#lists=[(int(x[0]),int(x[1]),int(x[2])) for x in [ln.rstrip('\n').split(',') for ln in open(sys.argv[1])]]
#print('{}'.format(lists))
col2analyze=int(sys.argv[2])
lg_base=2
# each line in lists is an experimental trial
if len(sys.argv) >= 5:
  n0 = int(sys.argv[4])  # lowest n
else:
  n0 = 0
if len(sys.argv) >= 6:
  n1 = int(sys.argv[5])  # highest n
else:
  n1 = max( [k[0] for k in lists] )    # is this assumption valid??
  print('warning: using highest n = {}, check if this is valid'.format(n1))
if len(sys.argv) >= 7:
  n2 = int(sys.argv[6])-1  # confirmation max n
else:
  n2 = max( [k[0] for k in lists] )    # is this assumption valid??
  print('warning: using max confirmation n = {}, check if this is valid'.format(n2))
print('using n between {} and {}, confirming to {}'.format(n0,n1,n2))
j = 0
d_x, d_y = [], []
while j < len(lists):
  if lists[j][0] <= n2:
    d_x.append(lists[j][0])
    d_y.append(lists[j][col2analyze])
  else:
    break
  #print('appending {}  {}'.format(lists[j][0], lists[j][col2analyze]))
  j+=1
running_max_x, running_max_y = running_max(lists,n0,n2,col2analyze)
mx_x, mx_y = left_endpoints(running_max_x,running_max_y,n2)
mn_x, mn_y = right_endpoints(running_max_x,running_max_y,n2)
# check the affect of doubling n
running_max = []
j = 0
while j < len(running_max_x):
  running_max.append((running_max_x[j],running_max_y[j]))
  j += 1
k = 2
j = 0
powers_x, powers_y = [], []
while j < len(running_max):
  if running_max[j][0] == k:
    powers_x.append(running_max[j][0])
    powers_y.append(running_max[j][1])
    k *= 2
  j += 1
growth_x, growth_y = [], []
cnt = 1
j = 1
while j < len(powers_x):
  growth_x.append(powers_x[j])
  growth_y.append(float(powers_y[j]/powers_y[j-1]))
  cnt += 1
  j += 1
print('growth2: {} {}'.format(growth_x,growth_y))

from_six_x, from_six_y = [], []
k = 6
j = 0
while j < len(running_max):
  if running_max[j][0] == k:
    from_six_x.append(running_max[j][0])
    from_six_y.append(running_max[j][1])
    k *= 2
  j += 1
growth_six_x, growth_six_y = [], []
cnt = 1
j = 1
while j < len(from_six_x):
  growth_six_x.append(from_six_x[j])
  growth_six_y.append(float(from_six_y[j]/from_six_y[j-1]))
  cnt += 1
  j += 1
print('growth6: {} {}'.format(growth_six_x,growth_six_y))


#m_best, b_best = loglog_regression(mx_x, mx_y)
m_best, b_best = find_bound(mx_x, mx_y, min_x=n0, max_x=n1, eps=0.00001)

upper_bound = lambda x: (b_best) * (x**m_best)
lower_bound = lambda x: 2 * x

cj1_x, cj1_y = conjecture_points(d_x, upper_bound)
cj2_x, cj2_y = conjecture_points(d_x, lower_bound)

upper_errors = confirm_upper_bound(d_x, d_y, upper_bound, min_x=n0, max_x=n2)
lower_errors = confirm_lower_bound(d_x, d_y, lower_bound, min_x=n0, max_x=n2)

fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(d_x,d_y,label='column {} (cache size)'.format(col2analyze))
ax.plot(running_max_x,running_max_y,label='running max of column {}'.format(col2analyze))

ax.plot(mx_x,mx_y,'o',label='left endpoints')
#ax.loglog(mx_x, mx_y, 'o', basex=2, basey=2, label='left_endpoints')

#ax.plot(mn_x,mn_y,'x',label='right endpoints')
ax.plot(cj1_x,cj1_y,'*',label='upper bound')
ax.plot(cj2_x,cj2_y,'--',label='lower bound')
#ax.plot(powers_x,powers_y,'*',label='powers')

# look at growth
#ax.plot(growth_x,growth_y,label='growth2')
#ax.plot(growth_six_x,growth_six_y,label='growth6')

ax.legend(loc='upper left')
plt.xlabel('problem size (n)')
plt.ylabel('critical cache size')
t = 'OLCS4 traceback with LRU, critical cache size as function of n\n'
t+= 'sample n is between {} and {}, '.format(n0, n1)
t+= 'confirmation n is between {} and {}'.format(n0, n2)
t+= '\nupper bound errors = {}, lower bound errors = {}'.format(upper_errors, lower_errors)
t+= '\nupper bound f(n)=({})n^({})'.format(b_best, m_best)
t+= ', lower bound g(n)=2n'
plt.title(t)
plt.show()
