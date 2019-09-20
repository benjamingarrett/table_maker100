import csv,itertools,os
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from math import e,log,sqrt

plot_line_types = ['-','--','-.',':']
plot_colors = ['b','g','r','c','m','y','k']

plot_1=True

if plot_1:
  results_path='./fib_results'
  f=lambda x: x if len(x)>0 else '0'
  d=os.listdir(results_path)
  ds=[]
  for fname in d:
    if 'csv' in fname:
      n=int([line.rstrip('\n').split(',') for line in open(results_path+'/'+fname)][0][1])
      ds.append((n,fname))
  ds.sort(key=lambda x: x[0])
  fig=plt.figure()
  ax=fig.add_subplot(111)
  color_idx=0
  line_type_idx=0
  for item in ds:
    new_list=[line.rstrip('\n').split(',') for line in open(results_path+'/'+item[1])]
    n=int(new_list[0][1])
    new_list=[[f(x[0]),f(x[1])] for x in new_list]
    x=[int(j) for j in [k[0] for k in new_list][1:]]
    y=[int(j) for j in [k[1] for k in new_list][1:]]
    print(x)
    print(y)
    color=plot_colors[color_idx]
    line_type=plot_line_types[line_type_idx]
    line_spec=color+line_type
    label_='n='+str(n)
    ax.plot(x,y,line_spec,linewidth=1,label=label_)
    color_idx=(color_idx+1)%len(plot_colors)
    line_type_idx=(line_type_idx+1)%len(plot_line_types)
  plt.xlabel('cache size')
  plt.ylabel('cache misses')
  ax.legend(loc='upper right')
  t='Fibonacci, LRU, Version 2, plot of tradeoff between cache size and cache misses'
  plt.title(t)
  plt.show()
