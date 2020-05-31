# Usage: python olcs4_..comparison.py <folder_with_csv's> [<col_to_plot>=1]
# Description: assumes that each csv file has a header in the first row
#              assumes plotting second column


import csv,os,sys,matplotlib as plt
from math import log,sqrt
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


print('{}'.format(sys.argv))
fig = plt.figure()
ax = fig.add_subplot(111)
for fn in [f for f in os.listdir(sys.argv[1]) if 'csv' in f]:
  #tmp_str = fn[15:]
  #print('tmp_str-->{}<--'.format(tmp_str))
  #b = int(tmp_str[0:tmp_str.find('.')])
  #print('b={}'.format(b))
  lst = [ln.rstrip('\n').split(',') for ln in open(sys.argv[1]+'/'+fn)]
  #print('{}'.format(fn))
  #print(lst)
  #print('----')
  j = 1  # assume header
  x = []
  y = []
  while j < len(lst):
    x.append(int(lst[j][0]))
    y.append(int(lst[j][1]))
    j += 1
  #if b < 8:
  ax.plot(x, y, label='file={}'.format(fn))
  #ax.loglog(x, y, basex=2, basey=2, label='b={}'.format(b))
plt.xlabel('problem size (n)')
plt.ylabel('critical cache size')
ax.legend(loc='upper left')
t = 'OLCS v4 traceback, LRU, critical cache size'
t+= '\nInstance type: 0^a 1^a ... (b-1)^(n mod a), a = ceiling(n/b), 1 <= b <= 14'
#t+= '\n                0^a 1^a ... (b-1)^a b^(n mod a), a = floor(n^c), b = floor(n/a), 0 < c < 1'
plt.title(t)
plt.show()
