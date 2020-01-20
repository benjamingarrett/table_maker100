import csv,itertools,os
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from math import e,log,sqrt
import sys

plot_line_types = ['-','--','-.',':']
plot_colors = ['b','g','r','c','m','y','k']

plot_1=None
plot_2=None
plot_3=True
plot_4=None
plot_5=None
plot_6=None
plot_7=None

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

def m(n):
  if n==1:
    return 1
  if n==2:
    return 3
  if n==3:
    return 5
  if n==4:
    return 8
  return m(n-1)+m(n-4)+2

def m_0a(n):
  if n==1:
    return 1
  if n==2:
    return 3
  if n==3:
    return 5
  if n==4:
    return 8
  f=[1,3,5,8]
  n_j=5
  while n_j<n:
    f.append(f[3]+f[0]+2)
    f.pop(0)
    n_j+=1
  return f[-1]

# for version 0a
if plot_2:
  x=list(range(7,int(sys.argv[1])))
  y=[m_0a(k) for k in x]
  lgy=[log(k,2) for k in y]
  m,b,r,p,std_err=stats.linregress(x,lgy)
  print('{} {} {} {} {}'.format(m,b,r,p,std_err))
  plgy=[m*k+b for k in x]
  B=2**b
  B=2.63
  qy=[B*2**(m*k) for k in x]
  dy=[abs(qy[j]-y[j]) for j,k in enumerate(x)]

  fig=plt.figure()
  ax=fig.add_subplot(111)

  #ax.plot(x,lgy)
  #ax.plot(x,plgy)
  #ax.plot(x,dy)
  ax.semilogy(x,dy)

  #ax.plot(x,y,label='M(n) = M(n-1)+M(n-4)+2')
  #ax.plot(x,qy,label='approximation')

  #ax.semilogy(x,y,label='M(n) = M(n-1)+M(n-4)+2')
  #ax.semilogy(x,qy,label='approximation')

  ax.legend(loc='upper left')
  plt.xlabel('cache size')
  plt.ylabel('cache misses')
  t = 'Fibonacci version 0a, LRU, cache size = 2\n'
  t+= 'Original conjecture: M(n) = M(n-1)+M(n-4)+2\n'
  t+= 'Approximated conjecture: M(n) = {}*2^({}*n) when n>=7'.format(2**b,m)
  plt.title(t)
  plt.show()
  print('Conjecture: M(n) = {}x2^({}xn)'.format(2**b,m))

def m_0c(n):
  if n==1:
    return 1
  if n==2:
    return 3
  if n==3:
    return 5
  if n%2==0:
    return m_0c(n-1)+1
  else:
    return 2*m_0c(n-1)

def m_0c_even(n):
  if n==1:
    return 1
  if n==2:
    return 3
  if n==3:
    return 5
  if n==4:
    return 6
  return 2*m_0c_even(n-2)+1

def m_0c_even_iter(n):
  if n%2!=0:
    print("m_0c_even_iter needs even integers: {}".format(n))
    exit()
  if n==2:
    return 3
  if n==4:
    return 6
  f=[3,6]
  n_j=4
  while n_j<n:
    f.append(2*f[1]+1)
    f.pop(0)
    n_j+=2
  return f[-1]

def m_0c_odd(n):
  if n==1:
    return 1
  if n==2:
    return 3
  if n==3:
    return 5
  if n==4:
    return 6
  return 2*m_0c_odd(n-2)+2

def m_0c_odd_iter(n):
  if n%2==0:
    print("m_0c_odd_iter needs odd integers: {}".format(n))
    exit()
  if n==1:
    return 1
  if n==3:
    return 5
  f=[1,5]
  n_j=3
  while n_j<n:
    f.append(2*f[1]+2)
    f.pop(0)
    n_j+=2
  return f[-1]

# for version 0c
if plot_3:
  x=list(range(1,int(sys.argv[1]),2))
  y=[m_0c_odd_iter(k) for k in x]
  #print("x {}".format(x))
  #print("y {}".format(y))
  #exit()
  lgy=[log(k,2) for k in y]
  m,b,r,p,std_err=stats.linregress(x,lgy)
  print('{} {} {} {} {}'.format(m,b,r,p,std_err))
  plgy=[m*k+b for k in x]
  qy=[(2**b)*2**(m*k) for k in x]

  fig=plt.figure()
  ax=fig.add_subplot(111)

  #ax.plot(x,lgy)
  #ax.plot(x,plgy)

  ax.plot(x,y,label='M(n) = M(n-1)+1 if even else 2M(n-1)')
  ax.plot(x,qy,label='approximation')

  #ax.semilogy(x,y)
  #ax.semilogy(x,qy)

  ax.legend(loc='upper left')
  plt.xlabel('cache size')
  plt.ylabel('cache misses')
  t = 'Fibonacci version 0c, LRU, cache size = 1\n'
  t+= 'Original conjecture: M(n) = M(n-1)+1 if even else 2M(n-1)\n'
  t+= 'Approximated conjecture: M(n) = {}*2^({}*n) when n>=1'.format(2**b,m)
  plt.title(t)
  plt.show()
  print('Conjecture: M(n) = {}x2^({}xn)'.format(2**b,m))

# for version 0c to see how constants converge
if plot_4:
  x=[40,80,160,320,640,960,980]
  y=[1.6947301,1.8703839,1.9709684,2.0247912,2.0526324,2.0620541,2.0624401]
  fig=plt.figure()
  ax=fig.add_subplot(111)
  ax.plot(x,y,label='constant multiple for approximation of M(n) = M(n-1)+1 if even else 2M(n-1)')
  ax.legend(loc='lower right')
  plt.xlabel('highest n for which f(n) computed')
  plt.ylabel('constant multiple')
  t = 'Fibonacci version 0c, LRU, cache size = 1\n'
  t+= 'Original conjecture: M(n) = M(n-1)+1 if even else 2M(n-1)\n'
  t+= 'Plot of constant multiple of approximation as higher values of f(n) are computed'
  plt.title(t)
  plt.show()

# for version 0c to see how constants converge - for constant in exponent
if plot_5:
  x=[40,80,160,320,640,960,980]
  y=[0.5103288,0.5027590,0.5007119,0.5001808,0.5000455,0.5000203,0.5000194]
  fig=plt.figure()
  ax=fig.add_subplot(111)
  ax.plot(x,y,label='constant multiple in exponent for approximation of M(n) = M(n-1)+1 if even else 2M(n-1)')
  ax.legend(loc='upper right')
  plt.xlabel('highest n for which f(n) computed')
  plt.ylabel('constant multiple in exponent')
  t = 'Fibonacci version 0c, LRU, cache size = 1\n'
  t+= 'Original conjecture: M(n) = M(n-1)+1 if even else 2M(n-1)\n'
  t+= 'Plot of constant multiple in exponent of approximation as higher values of f(n) are computed'
  plt.title(t)
  plt.show()


# for version 0a to see how constants converge
if plot_6:
  x=[20,40,80,160,320,640,1280]
  y=[
  1.6705976034394805,
  1.8060773254956186,
  1.8623693263793406,
  1.886542855328482,
  1.8976156826206572,
  1.9029012717662863,
  1.9054819206411202
  ]
  fig=plt.figure()
  ax=fig.add_subplot(111)
  ax.plot(x,y,label='constant multiple for approximation of M(n) = M(n-1)+M(n-4)+2')
  ax.legend(loc='lower right')
  plt.xlabel('highest n for which f(n) computed')
  plt.ylabel('constant multiple')
  t = 'Fibonacci version 0a, LRU, cache size = 1\n'
  t+= 'Original conjecture: M(n) = M(n-1)+M(n-4)+2\n'
  t+= 'Plot of constant multiple of approximation as higher values of f(n) are computed'
  plt.title(t)
  plt.show()

# for version 0a to see how constants converge - for constant in exponent
if plot_7:
  x=[20,40,80,160,320,640,1280]
  y=[
  0.47596848801249364,
  0.4675665897578548,
  0.46557225419264125,
  0.4651066184235827,
  0.46499479938027666,
  0.4649674289814365,
  0.46496065968039896]
  fig=plt.figure()
  ax=fig.add_subplot(111)
  ax.plot(x,y,label='constant multiple in exponent for approximation of M(n) = M(n-1)+M(n-4)+2')
  ax.legend(loc='upper right')
  plt.xlabel('highest n for which f(n) computed')
  plt.ylabel('constant multiple in exponent')
  t = 'Fibonacci version 0a, LRU, cache size = 1\n'
  t+= 'Original conjecture: M(n) = M(n-1)+M(n-4)+2\n'
  t+= 'Plot of constant multiple in exponent of approximation as higher values of f(n) are computed'
  plt.title(t)
  plt.show()

# for version 0a 
