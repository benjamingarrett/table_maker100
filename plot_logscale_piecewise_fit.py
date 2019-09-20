import os
from math import log
import matplotlib.pyplot as plt
from plot_piecewise import do_piecewise_regression

results_path = './lcs_results'
f = lambda x: x if len(x) > 0 else '0'

def create_piecewise_regression_log_plots(fname,extrema):
  new_list = [line.rstrip('\n').split(',') for line in open(results_path+'/'+fname)]
  n = int(new_list[0][1][0:new_list[0][1].find('-')])
  print(n)
  new_list = [[f(x[0]),f(x[1])] for x in new_list]
  x = [int(j) for j in [k[0] for k in new_list][1:]][0:-1]
  y = [int(j) for j in [k[1] for k in new_list][1:]][0:-1]
  y_dict = {}
  for i,xx in enumerate(x):
    #print('{} {} {}'.format(i,xx,y[i]))
    if extrema[n][0] < y[i] and y[i] < extrema[n][1]:
      if y[i] not in y_dict:
        y_dict[y[i]] = [xx]
      else:
        y_dict[y[i]].append(xx)
  merged = {}
  selected = {}
  for yy,L in y_dict.items():
    min_x = min(L)
    NL = []
    for xx in L:
      NL.append(min_x)
    merged[yy] = NL
    selected[yy] = min_x
  merged_x = []
  merged_y = []
  for yy,L in merged.items():
    for xx in L:
      merged_x.append(xx)
      merged_y.append(yy)
  selected_x = []
  selected_y = []
  for yy,xx in selected.items():
    selected_x.append(xx)
    selected_y.append(yy)
  lgx = [log(k) for k in merged_x]
  lgy = [log(k) for k in merged_y]
  (x_hat,y_hat,breaks) = do_piecewise_regression(lgx,lgy)
  lgx = [log(k) for k in selected_x]
  lgy = [log(k) for k in selected_y]
  (x_hat2,y_hat2,breaks2) = do_piecewise_regression(lgx,lgy)
  fig,ax = plt.subplots()
  ax.plot(lgx,lgy,'o',label='data')
  ax.plot(x_hat,y_hat,'k--',label='piecewise regression for merged points, breakpoint='+str(breaks[1]))
  ax.plot(x_hat2,y_hat2,'k:',label='piecewise regression for selected points, breakpoint='+str(breaks2[1]))
  ax.legend(loc='upper right')
  ax.set_xlabel('log(cache size)')
  ax.set_ylabel('log(cache misses)')
  t = 'LCS traceback, LRU, instance type: 0^k 1^k, log-log plot of tradeoff between cache size and cache misses, N = '+str(n)
  plt.title(t)
  plt.show()

# 5.25858
#===========================
extrema = {
  20: (800, 2800),
  30: (1600, 10000),
  40: (3000, 20000),
  50: (4000, 40000),
  60: (5000, 67002),
  70: (7400, 100000)}
for j in range(1,7):
  create_piecewise_regression_log_plots('cache_misses_000_111_'+str(j),extrema)
  #break
exit()



d = os.listdir(results_path)
lists = [] # why?
cnt = 1
#fig = plt.figure()
#ax = fig.add_subplot(111)
for new_field in d:
  new_list = [line.rstrip('\n').split(',') for line in open(results_path+'/'+new_field)]
  n = int(new_list[0][1][0:new_list[0][1].find('-')])
  print(n)
  #print(new_list)
  new_list = [[f(x[0]),f(x[1])] for x in new_list]
  x = [int(j) for j in [k[0] for k in new_list][1:]][0:-1]
  y = [int(j) for j in [k[1] for k in new_list][1:]][0:-1]
  #print(x)
  #print(y)
  #plt.plot(x,y,'o')
  #plt.show()
  selected_x = []
  selected_y = []
  for j,k in enumerate(x):
    selected_x.append(k)
    selected_y.append(y[j])
  x_dict = {}
  for j,k in enumerate(selected_x):
    x_dict[k] = selected_y[j]
  y_dict = {}
  for k,v in x_dict.items():
    y_dict[v] = -1
  min_y_dict = {}
  for item in y_dict:
    tmp = []
    for xval in selected_x:
      if x_dict[xval] == item:
        tmp.append(xval)
    min_y_dict[item] = min(tmp)
  sweet_x = []
  sweet_y = []
  for k,v in min_y_dict.items():
    sweet_x.append(v)
    sweet_y.append(k)
  print(sweet_x)
  print(sweet_y)
  sweet_x = sweet_x[5:-1]
  sweet_y = sweet_y[5:-1]
  print(sweet_x)
  print(sweet_y)
  plt.plot(sweet_x,sweet_y,'o')
  plt.title(str(n))
  plt.show()
  lgx = [log(k) for k in sweet_x]
  lgy = [log(k) for k in sweet_y]
  #plt.plot(lgx,lgy,'o')
  #plt.show()
  do_piecewise_regression(lgx,lgy)
  #break
