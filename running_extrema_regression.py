import csv,os,sys,matplotlib as plt
from math import log
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


def running_max(data,n0,n2):
  running_max_x = [data[n0][0]]
  running_max_y = [data[n0][2]]
  j = n0
  while j<=n2:
    running_max_x.append(data[j][0])
    if data[j][2] > running_max_y[-1]:
      running_max_y.append(data[j][2])
    else:
      running_max_y.append(running_max_y[-1])
    j+=1
  return running_max_x, running_max_y


def running_min(data,n0,n2):
  running_min_x = [data[n0][0]]
  running_min_y = [data[n0][2]]
  j = n0
  while j<=n2:
    running_min_x.append(data[j][0])
    if data[j][2] < running_min_y[-1]:
      running_min_y.append(data[j][2])
    else:
      running_min_y.append(running_max_y[-1])
    j+=1
  return running_min_x, running_min_y


def left_endpoints(x,y,n1):
  mx_x=[]
  mx_y=[]
  j=0
  while x[j]<=n1:
    if y[j] > y[j-1]:
      mx_x.append(x[j])
      mx_y.append(y[j])
    j+=1
  return mx_x, mx_y


def right_endpoints(x,y,n1):
  mn_x=[]
  mn_y=[]
  j=0
  while x[j]<=n1:
    if y[j] > y[j-1]:
      mn_x.append(x[j-1])
      mn_y.append(y[j-1])
    j+=1
  return mn_x, mn_y


def semilogx_regression(x,y,basex=2):
  lgx = [log(k,basex) for k in x]
  m, b, r, p, err = stats.linregress(lgx,y)
  return m, b


def first_method(mx_x,mx_y,mn_x,mn_y,m_upper,b_upper,m_lower,b_lower,basex=2,eps=0.0001):
  b_upper_best = b_upper
  success = False
  while not success:
    j = 0
    b_upper_best += eps
    while j<len(mx_x):
      if m_upper*log(mx_x[j],basex)+b_upper_best < mx_y[j]:
        success = False
        break
      else:
        success = True
      j += 1
    #print('{} {}'.format(success,b_upper_best))
  b_lower_best = b_lower
  success = False
  while not success:
    j = 0
    b_lower_best -= eps
    while j<len(mn_x):
      if m_lower*log(mn_x[j],basex)+b_lower_best > mn_y[j]:
        success = False
        break
      else:
        success = True
      j += 1
    #print('{} {}'.format(success,b_lower_best))
  return m_upper, b_upper_best, m_lower, b_lower_best


def second_method(mx_x,mx_y,mn_x,mn_y,m_upper,b_upper,m_lower,b_lower,basex=2,eps=0.0001):
  m_upper_best = m_upper
  success = False
  while not success:
    j = 0
    m_upper_best += eps
    while j<len(mx_x):
      if m_upper_best*log(mx_x[j],basex)+b_upper < mx_y[j]:
        success = False
        break
      else:
        success = True
      j += 1
    #print('{} {}'.format(success,m_upper_best))
  m_lower_best = m_lower
  success = False
  while not success:
    j = 0
    m_lower_best -= eps
    while j<len(mn_x):
      if m_lower_best*log(mn_x[j],basex)+b_lower > mn_y[j]:
        success = False
        break
      else:
        success = True
      j += 1
    #print('{} {}'.format(success,m_lower_best))
  return m_upper_best, b_upper, m_lower_best, b_lower


def confirm_conjecture(m_upper,b_upper,m_lower,b_lower,data_x,data_y,basex=2):
  upper_errors = 0
  lower_errors = 0
  j = 0
  while j<len(data_x):
    if data_y[j] > m_upper*log(data_x[j],basex)+b_upper:
      upper_errors += 1
    if data_y[j] < m_lower*log(data_x[j],basex)+b_lower:
      lower_errors += 1
    j += 1
  return upper_errors, lower_errors


lists=[(int(x[0]),int(x[1]),int(x[2])) for x in [ln.rstrip('\n').split(',') for ln in open(sys.argv[1])]]
lg_base=2
# each item in lists is an experimental trial
if len(sys.argv) >= 3:
  n0 = int(sys.argv[2])-1 # lowest n
else:
  n0 = 0
if len(sys.argv) >= 4:
  n1 = int(sys.argv[3])-1 # highest n
else:
  n1 = len(lists)-1
if len(sys.argv) >= 5:
  n2 = int(sys.argv[4])-1 # confirmation max n
else:
  n2 = len(lists)-1
print('using n between {} and {}, confirming to {}'.format(n0,n1,n2))
j = n0
d_x, d_y = [], []
while j<=n2:
  d_x.append(lists[j][0])
  d_y.append(lists[j][2])
  j+=1
running_max_x, running_max_y = running_max(lists,n0,n2)
if False:
  j=0
  with open('running_max','w') as fp:
    fp.write('running max\n')
    while j<len(running_max_x):
      fp.write('{} {}\n'.format(running_max_x[j],running_max_y[j]))
      j+=1
  exit()
mx_x, mx_y = left_endpoints(running_max_x,running_max_y,n1)
mn_x, mn_y = right_endpoints(running_max_x,running_max_y,n1)
if False:
  j=0
  with open('leftendpoints','w') as fp:
    fp.write('leftendpoints\n')
    while j<len(mx_x):
      fp.write('{} {}\n'.format(mx_x[j],mx_y[j]))
      j+=1
  j=0
  with open('rightendpoints','w') as fp:
    fp.write('rightendpoints\n')
    while j<len(mn_x):
      fp.write('{} {}\n'.format(mn_x[j],mn_y[j]))
      j+=1
  exit()
m_max, b_max = semilogx_regression(mx_x,mx_y,lg_base)
m_min, b_min = semilogx_regression(mn_x,mn_y,lg_base)

bound_x = [lists[n0][0],lists[n1][0]]
conjecture_x = [lists[n0][0],lists[n2][0]]

# method 0 - original regression
upper_y = [m_max*log(lists[n0][0],lg_base)+b_max,m_max*log(lists[n1][0],lg_base)+b_max]
lower_y = [m_min*log(lists[n0][0],lg_base)+b_min,m_min*log(lists[n1][0],lg_base)+b_min]

# method 1 - adjust y-intercept to bound sample data
m_upper_first, b_upper_first, m_lower_first, b_lower_first = first_method(mx_x,mx_y,mn_x,mn_y,m_max,b_max,m_min,b_min)
m_upper_first_r, b_upper_first_r, m_lower_first_r, b_lower_first_r = first_method(running_max_x[0:n1],running_max_y[0:n1],running_max_x[0:n1],running_max_y[0:n1],m_max,b_max,m_min,b_min)
print('using endpoints {} {} {} {}'.format(m_upper_first, b_upper_first, m_lower_first, b_lower_first))
print('Use running max {} {} {} {}'.format(m_upper_first_r, b_upper_first_r, m_lower_first_r, b_lower_first_r))
upper_y_first = [m_upper_first*log(lists[n0][0],lg_base)+b_upper_first, m_upper_first*log(lists[n2][0],lg_base)+b_upper_first]
lower_y_first = [m_lower_first*log(lists[n0][0],lg_base)+b_lower_first, m_lower_first*log(lists[n2][0],lg_base)+b_lower_first]
up_errors_1,lo_errors_1 = confirm_conjecture(m_upper_first,b_upper_first,m_lower_first,b_lower_first,running_max_x,running_max_y)

# method 2 - adjust slope to bound sample data
m_upper_second, b_upper_second, m_lower_second, b_lower_second = second_method(mx_x,mx_y,mn_x,mn_y,m_max,b_max,m_min,b_min)
m_upper_second_r, b_upper_second_r, m_lower_second_r, b_lower_second_r = second_method(running_max_x[0:n1],running_max_y[0:n1],running_max_x[0:n1],running_max_y[0:n1],m_max,b_max,m_min,b_min)
print('using endpoints {} {} {} {}'.format(m_upper_second, b_upper_second, m_lower_second, b_lower_second))
print('Use running max {} {} {} {}'.format(m_upper_second_r, b_upper_second_r, m_lower_second_r, b_lower_second_r))
upper_y_second = [m_upper_second*log(lists[n0][0],lg_base)+b_upper_second, m_upper_second*log(lists[n2][0],lg_base)+b_upper_second]
lower_y_second = [m_lower_second*log(lists[n0][0],lg_base)+b_lower_second, m_lower_second*log(lists[n2][0],lg_base)+b_lower_second]
up_errors_2,lo_errors_2 = confirm_conjecture(m_upper_second,b_upper_second,m_lower_second,b_lower_second,running_max_x,running_max_y)

# method 3 - use the intercept from first method and slope from second method
upper_y_third = [m_upper_second*log(lists[n0][0],lg_base)+b_upper_first, m_upper_second*log(lists[n2][0],lg_base)+b_upper_first]
lower_y_third = [m_lower_second*log(lists[n0][0],lg_base)+b_lower_first, m_lower_second*log(lists[n2][0],lg_base)+b_lower_first]
up_errors_3,lo_errors_3 = confirm_conjecture(m_upper_second,b_upper_first,m_lower_second,b_lower_second,running_max_x,running_max_y)


#-----------------------------------------------------------
# bounding running min
#running_min_x, running_min_y = running_min(lists,n0,n2)

# left endpoints
#left_EP_min_x, left_EP_min_y = left_endpoints(running_min_x,running_min_y,n1)

# right endpoints
#right_EP_min_x, right_EP_min_y = right_endpoints(running_min_x,running_min_y,n1)

# regression of left and right endpoints for running min
#m_max, b_max = semilogx_regression(left_EP_min_x,left_EP_min_y,lg_base)
#m_min, b_min = semilogx_regression(right_EP_min_x,right_EP_min_y,lg_base)

# method 2 - adjust slope to bound sample data
#m_upper_second, b_upper_second, m_lower_second, b_lower_second = second_method(mx_x,mx_y,mn_x,mn_y,m_max,b_max,m_min,b_min)
#m_upper_second_r, b_upper_second_r, m_lower_second_r, b_lower_second_r = second_method(running_min_x[0:n1],running_min_y[0:n1],running_min_x[0:n1],running_min_y[0:n1],m_max,b_max,m_min,b_min)
#print('using endpoints {} {} {} {}'.format(m_upper_second, b_upper_second, m_lower_second, b_lower_second))
#print('Use running max {} {} {} {}'.format(m_upper_second_r, b_upper_second_r, m_lower_second_r, b_lower_second_r))
#upper_y_second = [m_upper_second*log(lists[n0][0],lg_base)+b_upper_second, m_upper_second*log(lists[n2][0],lg_base)+b_upper_second]
#lower_y_second = [m_lower_second*log(lists[n0][0],lg_base)+b_lower_second, m_lower_second*log(lists[n2][0],lg_base)+b_lower_second]
#up_errors_2,lo_errors_2 = confirm_conjecture(m_upper_second,b_upper_second,m_lower_second,b_lower_second,running_max_x,running_max_y)


fig = plt.figure()
ax = fig.add_subplot(111)
ax.semilogx(d_x,d_y,basex=lg_base,label='min cache misses for problem size (original data)')
ax.semilogx(running_max_x,running_max_y,basex=lg_base,label='running max of min cache misses')
ax.semilogx(mx_x,mx_y,'o',basex=lg_base,label='left endpoints of running max')
ax.semilogx(mn_x,mn_y,'*',basex=lg_base,label='right endpoints of running max')
ax.semilogx(bound_x,lower_y,basex=lg_base,label='regression for right endpoints {} {}'.format(m_min,b_min))
ax.semilogx(bound_x,upper_y,basex=lg_base,label='regression for left endpoints {} {}'.format(m_max,b_max))
#ax.semilogx(conjecture_x,lower_y_first,basex=lg_base,label='lower (1st method) {} {} errors {}'.format(m_lower_first,b_lower_first,lo_errors_1))
#ax.semilogx(conjecture_x,upper_y_first,basex=lg_base,label='upper (1st method) {} {} errors {}'.format(m_upper_first,b_upper_first,up_errors_1))
ax.semilogx(conjecture_x,lower_y_second,basex=lg_base,label='lower (2nd method) {} {} errors {}'.format(m_lower_second,b_lower_second,lo_errors_2))
ax.semilogx(conjecture_x,upper_y_second,basex=lg_base,label='upper (2nd method) {} {} errors {}'.format(m_upper_second,b_upper_second,up_errors_2))
#ax.semilogx(conjecture_x,lower_y_third,basex=lg_base,label='lower (3rd method) {} {} errors {}'.format(m_lower_second,b_lower_first,lo_errors_3))
#ax.semilogx(conjecture_x,upper_y_third,basex=lg_base,label='upper (3rd method) {} {} errors {}'.format(m_upper_second,b_upper_first,up_errors_3))


ax.legend(loc='upper left')
plt.xlabel('problem size (n)')
plt.ylabel('min cache misses')
t = 'Fibonacci version 1a, minimum cache misses as a function of problem size\n'
t+= 'sample n is between {} and {}, '.format(lists[n0][0],lists[n1][0])
t+= 'confirmation n is between {} and {}\n'.format(lists[n0][0],lists[n2][0])
t+= '1st method: adjust y-intercept\n'
t+= '2nd method: adjust slope\n'
t+= '3rd method: use intercept from first, slope from second'
plt.title(t)
plt.show()

