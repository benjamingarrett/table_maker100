import matplotlib.pyplot as plt
from scipy import stats
import sys


def first_index_of(lst, x):
  j = 0
  while j < len(lst) and lst[j] <= x:
    j += 1
  if j < len(lst):
    return j
  else:
    return None


def last_index_of(lst, x):
  j = len(lst)-1
  while j >= 0 and lst[j] >= x:
    j -= 1
  if j >= 0:
    return j
  else:
    return None


def get_min_in_range(lst, x1, x2):
  j1 = first_index_of(lst, x1)
  j2 = last_index_of(lst, x2)
  if j1 is not None and j2 is not None:
    return (lst[first_index_of(lst, min(lst[j1:j2]))], min(lst[j1:j2]))
  else:
    return (None,None)


def get_max_in_range(lst, x1, x2):
  j1 = first_index_of(lst, x1)
  j2 = last_index_of(lst, x2)
  if j1 is not None and j2 is not None:
    return (lst[first_index_of(lst, max(lst[j1:j2]))], max(lst[j1:j2]))
  else:
    return (None,None)


plot_line_types=['-','--','-.',':']
plot_colors=['b','g','r','c','m','y','k']
lists=[ln.rstrip('\n').split(',') for ln in open(sys.argv[1])]
lowest_size=int(sys.argv[2])
#print(lists)
d = {}
fig=plt.figure()
ax=fig.add_subplot(111)
color_idx=0
line_type_idx=0
for k in lists[1:]:
  #if k[0]=='12' or k[0]=='11' or k[0]=='10' or k[0]=='9' or k[0]=='8' or k[0]=='7' or k[0]=='6' or k[0]=='5' or k[0]=='4' or k[0]=='3' or k[0]=='2' or k[0]=='1':
  if k[0]=='1':
    d[k[0]]=[int(g) for g in k[1:]]
    #print(d[k[0]])
    x=[i for i in range(lowest_size, lowest_size+len(d[k[0]]))]
    y=d[k[0]]
    m,b,r,p,err=stats.linregress(x,y)
    py=[m*i+b for i in x]
    diff=[k-py[i] for i,k in enumerate(y)]
    i = 1
    max_dif_x = [1]
    max_dif_y = [diff[0]]
    min_dif_x = [1]
    min_dif_y = [diff[0]]
    while i < len(diff):
      if diff[i] > max(max_dif_y):
        max_dif_x.append(i)
        max_dif_y.append(diff[i])
      if diff[i] < min(min_dif_y):
        min_dif_x.append(i)
        min_dif_y.append(diff[i])
      i += 1
    label_='cache size: '+k[0]+', m: '+str(m)+', b: '+str(b)
    color=plot_colors[color_idx]
    line_type=plot_line_types[line_type_idx]
    line_spec=color+line_type

    ax.plot(x,diff)

    #(max_diff_x1, max_diff_y1) = (514, 23.4523)
    #(max_diff_x2, max_diff_y2) = (1026, 35.2267)

    #(max_diff_x1, max_diff_y1) = (33, 11.2659)
    #(max_diff_x2, max_diff_y2) = (65, 12.0018)

    #m1 = (max_diff_y2-max_diff_y1)/(max_diff_x2-max_diff_x1)
    #b1 = max_diff_y1-m1*max_diff_x1
    #ax.plot([x[0],x[-1]],[m1*x[0]+b1,m1*x[-1]+b1])

    #(min_diff_x1, min_diff_y1) = (639, -25.0481)
    #(min_diff_x2, min_diff_y2) = (1279, -58.3302)

    #(min_diff_x1, min_diff_y1) = (38, 5.00584)
    #(min_diff_x2, min_diff_y2) = (78, 2.92574)

    #m2 = (min_diff_y2-min_diff_y1)/(min_diff_x2-min_diff_x1)
    #b2 = min_diff_y1-m2*min_diff_x1
    #ax.plot([x[0],x[-1]],[m2*x[0]+b2,m2*x[-1]+b2])
    
    #m1,b1,r1,p1,err1=stats.linregress(max_dif_x,max_dif_y)
    #ax.plot(max_dif_x,max_dif_y)
    #y1 = [m1*i+b1 for i in max_dif_x]
    #ax.plot(max_dif_x,y1)

    #m2,b2,r2,p2,err2=stats.linregress(min_dif_x,min_dif_y)
    #y2 = [m2*i+b2 for i in min_dif_x]
    #ax.plot(min_dif_x,y2)

    #ax.plot(x,len(x)*[0])
    #ax.plot(x,diff)
    #print(max_dif_y)
    #print(min_dif_y)
    #ax.plot(max_dif_x,max_dif_y)
    #ax.plot(min_dif_x,min_dif_y)

    if False:
      x1a = 318
      y1a = m*x1a+b+9.55506
      x2a = 639
      y2a = m*x2a+b+25.0481
      ma = (y2a-y1a)/(x2a-x1a)
      ba = y1a - ma*x1a

      x1b = 514
      y1b = m*x1b+b-23.4523
      x2b = 1026
      y2b = m*x2b+b-35.2267
      mb = (y2b-y1b)/(x2b-x1b)
      bb = y1b - mb*x1b

      label_='upper bound: cache misses <= '+str(ma)+' * N + '+str(ba)
      ax.plot(x,[ma*xi+ba for xi in x],label=label_)

      label_='lower bound: cache misses >= '+str(mb)+' * N + '+str(bb)
    
      ax.plot(x,[mb*xi+bb for xi in x],label=label_)

      #ax.plot([x1a,x2a],[y1a,y2a])
      #ax.plot([x1b,x2b],[y1b,y2b])

      ax.plot(x,y,line_spec,linewidth=1)
      #ax.plot(x,py,line_spec,linewidth=1)

    ax.plot(514, -23.4523, 'ro')
    ax.plot(1026, -35.2267, 'ro')
    ax.plot(318, 9.55506, 'ro')
    ax.plot(639, 25.0481, 'ro')

    color_idx=(color_idx+1)%len(plot_colors)
    line_type_idx=(line_type_idx+1)%len(plot_line_types)
plt.xlabel('problem size, N')
plt.ylabel('difference between observed cache misses and regression predicted cache misses')
#ax.legend(loc='upper left')
t = 'Fibonacci version 1a, cache size 1\n'
t+= 'Difference between data and regression line'
#t+= 'Plot of conjecture, Upper bound confirmed for N <= 10000, Lower bound invalid for N~=1020, N~=2048, N~=4100, N~=8100\n'
#t+= 'Constants for upper bound found using data at N = 514 & N = 1026, for lower bound using data at N = 318 & N = 639\n'
#t+= 'Because those values of N show maximal absolute difference from regression line fitted to data\n'
#t+= 'Conjecture: for version 1a of Fibonacci, cache size 1, m1*N+b1 <= cache misses <= m2*N+b2 (see constants in legend)'
plt.title(t)
plt.show()
