import csv,itertools,os,sys
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from math import e,log,sqrt

#this one for multi-segment 
from plot_piecewise import do_piecewise_regression

#see plot_tradeoff for single segment regression


#not this one
from piecewise import do_piecewise_linear

# plot 1: all instances, all data points, normal scale
# plot 2: collapsed points, normal scale
# plot 3: collapsed points, log-log scale, 1-segment regression
# plot 4: collapsed points, log-log scale, 2-segment regression
# plot 5: collapsed points, log-log scale, 3-segment regression
# plot 6: collapsed points, log-log scale, 4-segment regression
# plot 7: collapsed points, log-log scale, 5-segment regression

plot_line_types = ['-','--','-.',':']
plot_colors = ['b','g','r','c','m','y','k']

plot_1 = None
analysis_1 = True

plot_2 = None
plot_3 = None
plot_4 = None
plot_5 = None

def calculate_median(a):
  a = sorted(a)
  a_len = len(a)
  if a_len < 1:
    return None
  if a_len % 2 == 0:
    return (a[int((a_len-1)/2)] + a[int((a_len+1)/2)])/2.0
  else:
    return a[int((a_len-1)/2)]

def y_intercept(x1,y1,x2,y2):
  return y1 - (y2-y1)/(x2-x1)*x1

def get_best_prune_factor(x,y,n):
  pi = 5
  best = 0
  best_pi = pi
  increment = 0.01
  cnt = 0
  while True:
    print('get best prune factor trying pi = {}'.format(pi))
    remaining_indices = [i for i,xx in enumerate(x) if xx < (pi * n * sqrt(n))]
    if len(remaining_indices) > 0:
      px = [k for i,k in enumerate(x) if i in remaining_indices]
      py = [k for i,k in enumerate(y) if i in remaining_indices]
      slope_, intercept_, r_value, p_value, std_err = stats.linregress(px,py)
      q = abs(r_value**2)
      if best < q and q is not 1.0:
        best = q
        best_pi = pi
      else:
        cnt += 1
      print('quality = {}'.format(q))
      if q > 0.999 or (cnt > 1000 and best is not 0) :
        return best_pi
      pi -= increment
    else:
      return best_pi

# plot 1
if plot_1:
  #results_path = './lcs_results'
  #results_path = './lcs_results_1_sm'
  #results_path = './lcs_results_2_sm'
  #results_path = './kmp_ps'
  results_path = './kmp_ps_powers'
  f = lambda x: x if len(x) > 0 else '0'
  d = os.listdir(results_path)
  d = sorted(d)
  fig = plt.figure()
  ax = fig.add_subplot(111)
  color_idx = 0
  line_type_idx = 0
  min_y = sys.maxsize
  max_x = 0
  for new_field in d:
    new_list = [line.rstrip('\n').split(',') for line in open(results_path+'/'+new_field)]
    n = int(new_list[0][1][0:new_list[0][1].find('-')])
    new_list = [[f(x[0]),f(x[1])] for x in new_list]
    x = [int(j) for j in [k[0] for k in new_list][1:]][0:-1]
    y = [int(j) for j in [k[1] for k in new_list][1:]][0:-1]
    if False:
      cutoff = -1
      for i,xx in enumerate(x):
        if xx == y[i]:
          cutoff = i
          break
      if cutoff is not -1:
        remaining_indices = [k for k,xx in enumerate(x) if xx < cutoff]
        x = [xx for i,xx in enumerate(x) if i in remaining_indices]
        y = [yy for i,yy in enumerate(y) if i in remaining_indices]
    if True:
      regression_cutoff_factor = 0.09
      regression_cutoff = n * regression_cutoff_factor
      regression_cutoff = sqrt(n)
      regression_indices = [k for k,xx in enumerate(x) if xx < regression_cutoff]
      regression_x = [xx for i,xx in enumerate(x) if i in regression_indices]
      regression_y = [yy for i,yy in enumerate(y) if i in regression_indices]
      x = regression_x
      y = regression_y
    max_x = max(x) if max(x) > max_x else max_x
    min_y = min(y) if min(y) < min_y else min_y
    if True:
      lgx = [log(k,10) for k in x]
      lgy = [log(k,10) for k in y]
      slope_, intercept_, r_value, p_value, std_err = stats.linregress(lgx,lgy)
      m = slope_
      b = intercept_
      poly_fit_x = [10**k for k in lgx]
      poly_fit_y = [(10**b)*(k**m) for k in poly_fit_x]
      ax.loglog(poly_fit_x,poly_fit_y)
    color_idx = (color_idx + 1) % len(plot_colors)
    line_type_idx = (line_type_idx + 1) % len(plot_line_types)
    color = plot_colors[color_idx]
    line_type = plot_line_types[line_type_idx]
    marker_spec = color + 'o'
    line_spec = color + line_type
    label_ = 'n='+str(n)+',m='+str(m)+',b='+str(b)+',r^2='+str(float(r_value**2))+',max(x)='+str(regression_cutoff)
    #ax.plot(x,y,color='blue',linewidth=1)
    #ax.plot(x,y,line_spec,label=label_)
    ax.loglog(x,y,line_spec,label=label_)
    #ax.semilogx(x,y,line_spec,label=label_)
  t = 'prefix-suffix function of KMP, instance type: (a^(n-1))b, LRU'
  t += '\nwith regression equation y=(10^b)(x^m)'
  #t += '\ncache size cutoff factor = '+str(regression_cutoff_factor)
  t += '\ncache size cutoff factor: sqrt(n)'
  #ax.plot([min_y,max_x],[min_y,max_x],'k')
  plt.xlabel('cache size')
  plt.ylabel('cache misses')
  ax.legend(loc='upper right')
  plt.title(t)
  plt.show()

# analysis 1
if analysis_1:
  results_path = './kmp_ps_powers'
  f = lambda x: x if len(x) > 0 else '0'
  d = os.listdir(results_path)
  d = sorted(d)
  fig = plt.figure()
  ax = fig.add_subplot(111)
  c1 = 0.1
  c2 = 20.5
  for new_field in d:
    new_list = [line.rstrip('\n').split(',') for line in open(results_path+'/'+new_field)]
    n = int(new_list[0][1][0:new_list[0][1].find('-')])
    new_list = [[f(x[0]),f(x[1])] for x in new_list]
    x = [int(j) for j in [k[0] for k in new_list][1:]][0:-1]
    y = [int(j) for j in [k[1] for k in new_list][1:]][0:-1]
    prod = [y[j]*xx for j,xx in enumerate(x)]
    if True:
      #cutoff_factor = 0.09
      #cutoff = n*cutoff_factor
      cutoff = sqrt(n)
      good_indices = [k for k,xx in enumerate(x) if xx<cutoff]
      x = [xx for k,xx in enumerate(x) if k in good_indices]
      y = [yy for k,yy in enumerate(y) if k in good_indices]
      prod = [y[j]*xx for j,xx in enumerate(x)]
      c1 = min(prod)/n
      c2 = max(prod)/n
      print('for n = {} c1 = {} c2 = {}'.format(n,c1,c2))

      lower = [c1*n for xx in enumerate(x)]
      upper = [c2*n for xx in enumerate(x)]
      ax.plot(x,lower,'--')
      ax.plot(x,upper,':')
    ax.plot(x,prod)

  plt.show()


#c1 n <= size misses <= c2 n




# plot 2
if plot_2:
  #results_path = './lcs_results'
  #results_path = './lcs_results_1_sm'
  results_path = './lcs_results_2_sm'
  f = lambda x: x if len(x) > 0 else '0'
  d = os.listdir(results_path)
  fig = plt.figure()
  ax = fig.add_subplot(111)
  for new_field in d:
    new_list = [line.rstrip('\n').split(',') for line in open(results_path+'/'+new_field)]
    new_list = [[f(x[0]),f(x[1])] for x in new_list]
    x = [int(j) for j in [k[0] for k in new_list][1:]][0:-1]
    y = [int(j) for j in [k[1] for k in new_list][1:]][0:-1]
    print(len(x))
    collapsed_x = []
    collapsed_y = []
    for j,k in enumerate(x):
      collapsed_x.append(k)
      collapsed_y.append(y[j])
    x_dict = {}
    for j,k in enumerate(collapsed_x):
      x_dict[k] = collapsed_y[j]
    #ax.plot(x,y,color='blue',linewidth=1)
    y_dict = {}
    for k,v in x_dict.items():
      y_dict[v] = -1
    min_y_dict = {}
    y_list = list(y_dict.keys())
    sorted(y_list)
    highest_y = y_list[-1]
    print('highest y {}'.format(highest_y))
    low_y1 = y_list[0]
    print('low_y1 {}'.format(low_y1))
    low_y2 = y_list[1]
    print('low_y2 {}'.format(low_y2))
    low_y3 = y_list[2]
    print('low_y3 {}'.format(low_y3))
    collapsed = []
    for item in y_dict:
      if not(item==highest_y or item==low_y1 or item==low_y2 or item==low_y3):
        tmp = []
        for xval in collapsed_x:
          if x_dict[xval] == item:
            tmp.append(xval)
        for x_val in tmp:
          collapsed.append((min(tmp),item))
        min_y_dict[item] = min(tmp)
    collapsed_x = []
    collapsed_y = []
    for g in collapsed:
      collapsed_x.append(g[0])
      collapsed_y.append(g[1])
    for g in collapsed:
      print('{}'.format(g))
    for k,v in min_y_dict.items():
      print('{} {}'.format(k,v))
    #ax.plot(sweet_x,sweet_y,color='blue','o')
    ax.scatter(collapsed_x,collapsed_y,color='blue')
  plt.show()

# plot 3
if plot_3:
  #results_path = './lcs_results'
  #results_path = './lcs_results_1_sm'
  results_path = './lcs_results_2_sm'
  f = lambda x: x if len(x) > 0 else '0'
  d = os.listdir(results_path)
  fig = plt.figure()
  ax = fig.add_subplot(111)
  for new_field in d:
    new_list = [line.rstrip('\n').split(',') for line in open(results_path+'/'+new_field)]
    new_list = [[f(x[0]),f(x[1])] for x in new_list]
    x = [int(j) for j in [k[0] for k in new_list][1:]][0:-1]
    y = [int(j) for j in [k[1] for k in new_list][1:]][0:-1]
    #print(len(x))
    collapsed_x = []
    collapsed_y = []
    for j,k in enumerate(x):
      collapsed_x.append(k)
      collapsed_y.append(y[j])
    x_dict = {}
    for j,k in enumerate(collapsed_x):
      x_dict[k] = collapsed_y[j]
    #ax.plot(x,y,color='blue',linewidth=1)
    y_dict = {}
    for k,v in x_dict.items():
      y_dict[v] = -1
    min_y_dict = {}
    y_list = list(y_dict.keys())
    sorted(y_list)
    highest_y = y_list[-1]
    print('highest y {}'.format(highest_y))
    low_y1 = y_list[0]
    print('low_y1 {}'.format(low_y1))
    low_y2 = y_list[1]
    print('low_y2 {}'.format(low_y2))
    low_y3 = y_list[2]
    print('low_y3 {}'.format(low_y3))
    collapsed = []
    for item in y_dict:
      if not(item==highest_y or item==low_y1 or item==low_y2 or item==low_y3):
        tmp = []
        for xval in collapsed_x:
          if x_dict[xval] == item:
            tmp.append(xval)
        for x_val in tmp:
          collapsed.append((min(tmp),item))
        min_y_dict[item] = min(tmp)
    collapsed_x = []
    collapsed_y = []
    for g in collapsed:
      collapsed_x.append(g[0])
      collapsed_y.append(g[1])
    #for g in collapsed:
    #  print('{}'.format(g))
    #for k,v in min_y_dict.items():
    #  print('{} {}'.format(k,v))
    #ax.plot(sweet_x,sweet_y,color='blue','o')
    p = np.polyfit(collapsed_x,collapsed_y,1)
    h = np.poly1d(p)

    ax.plot(collapsed_x,collapsed_y,'bo',markersize=3)
    ax.plot(collapsed_x,h(collapsed_x),'b-',label='PolyFit')

    #ax.loglog(collapsed_x,collapsed_y,'bo',markersize=3)
    #ax.loglog(collapsed_x,h(collapsed_x),'b-',label='PolyFit')

  plt.show()

# plot 4
if plot_4:
  #results_path = './lcs_results_1_sm'
  #results_path = './lcs_results_2_sm'
  #results_path = './lcs_results'
  #results_path = './lcs_binary_search'
  results_path = './lcs_temp'
  f = lambda x: x if len(x) > 0 else '0'
  d = os.listdir(results_path)
  d = sorted(d)
  fig = plt.figure()
  ax = fig.add_subplot(111)
  color_idx = 0
  line_type_idx = 0
  slope_data = []
  for new_field in d:
    new_list = [line.rstrip('\n').split(',') for line in open(results_path+'/'+new_field)]
    n = int(new_list[0][1][0:new_list[0][1].find('-')])
    #if True:
    #if n in {160}:
    #if n in {40,80,120,160,200,240}:
    if True and n>4:
      print('n = {}'.format(n))
      new_list = [[f(x[0]),f(x[1])] for x in new_list]
      x = [int(j) for j in [k[0] for k in new_list][1:]][0:-1]
      y = [int(j) for j in [k[1] for k in new_list][1:]][0:-1]

      collapsed_x = []
      collapsed_y = []
      for j,k in enumerate(x):
        collapsed_x.append(k)
        collapsed_y.append(y[j])
      x_dict = {}
      for j,k in enumerate(collapsed_x):
        x_dict[k] = collapsed_y[j]
      #ax.plot(x,y,color='blue',linewidth=1)
      y_dict = {}
      for k,v in x_dict.items():
        y_dict[v] = -1
      min_y_dict = {}
      y_list = list(y_dict.keys())
      sorted(y_list)
      highest_y = y_list[-1]
      print('highest y {}'.format(highest_y))
      low_y1 = y_list[0]
      print('low_y1 {}'.format(low_y1))
      low_y2 = y_list[1]
      print('low_y2 {}'.format(low_y2))
      low_y3 = y_list[2]
      print('low_y3 {}'.format(low_y3))
      collapsed = []
      selected = []
      for item in y_dict:
        if not(item==highest_y or item==low_y1 or item==low_y2 or item==low_y3):
          tmp = []
          for xval in collapsed_x:
            if x_dict[xval] == item:
              tmp.append(xval)
          for x_val in tmp:
            collapsed.append((min(tmp),item))
          min_y_dict[item] = min(tmp)
          selected.append((min(tmp),item))
      collapsed_x = []
      collapsed_y = []
      for g in collapsed:
        collapsed_x.append(g[0])
        collapsed_y.append(g[1])
      selected_x = []
      selected_y = []
      for g in selected:
        selected_x.append(g[0])
        selected_y.append(g[1])
      if True:
        chosen_x = collapsed_x
        chosen_y = collapsed_y
      else:
        chosen_x = selected_x
        chosen_y = selected_y
      lgx = [log(k,10) for k in chosen_x]
      lgy = [log(k,10) for k in chosen_y]

      # remove "last" sweet spot
      print('len lgx before removal {}'.format(len(lgx)))
      print('len lgy before removal {}'.format(len(lgy)))
      #max_times = 1 if n is not 40 else 2
      max_times = 0
      cnt = 0
      while cnt < max_times:
        lowest_x_indices = [i for i,xx in enumerate(lgx) if xx==min(lgx)]
        print('min lgx {}'.format(min(lgx)))
        print('lowest x indices {}'.format(lowest_x_indices))
        lgx = [k for i,k in enumerate(lgx) if i not in lowest_x_indices]
        lgy = [k for i,k in enumerate(lgy) if i not in lowest_x_indices]
        cnt += 1
      print('len lgx after removal {}'.format(len(lgx)))
      print('len lgy after removal {}'.format(len(lgy)))


      #p = np.polyfit(collapsed_x,collapsed_y,1)
      p = np.polyfit(lgx,lgy,1)
      h = np.poly1d(p)
      print('one piece p = {}'.format(p))


      slope_, intercept_, r_value, p_value, std_err = stats.linregress(lgx,lgy)
      print('scipy results {} {} {} {} {}'.format(slope_,intercept_,r_value,p_value,std_err))
      print('scipy coefficient of determination {}'.format(r_value**2))


      #(x_hat,y_hat,breaks) = do_piecewise_regression(collapsed_x,collapsed_y,2)
      #(x_hat,y_hat,breaks) = do_piecewise_regression(lgx,lgy,2)
      #print(collapsed_x[0])
      #print(log(collapsed_x[0]))

      # post-regression pruning - old way
      if False:
        max_times = 4
        cnt = 0
        while cnt < max_times:
          print('prune cnt {}'.format(cnt))
          x_median = calculate_median(lgx)
          far_right_indices = [i for i,xx in enumerate(lgx) if xx >= x_median]
          print('len far right indices {}'.format(len(far_right_indices)))
          removal_indices = [i for i,yy in enumerate(lgy) if i in far_right_indices and yy > h(lgx[i])]
          print('len removal indices {}'.format(len(removal_indices)))
          lgx = [k for i,k in enumerate(lgx) if i not in removal_indices]
          lgy = [k for i,k in enumerate(lgy) if i not in removal_indices]
          p,r1,r2,r3,r4 = np.polyfit(lgx,lgy,1,full=True)
          h = np.poly1d(p)
          print("---------")
          print("polyfit results {} {} {} {} {} {}".format(p,h,r1,r2,r3,r4))
          print("---------")
          cnt += 1

      # post-regression pruning - new way
      if True:
        while len(lgx) > 2:
          if abs(r_value**2) >= 0.999:
            break
          remaining_indices = [i for i,xx in enumerate(lgx) if xx != max(lgx)]
          lgx = [k for i,k in enumerate(lgx) if i in remaining_indices]
          lgy = [k for i,k in enumerate(lgy) if i in remaining_indices]
          #print('removed {} points now there are {} {} points'.format(len(remaining_indices),len(lgx),len(lgy)))
          slope_, intercept_, r_value, p_value, std_err = stats.linregress(lgx,lgy)
          #print('scipy results {} {} {} {} {}'.format(slope,intercept,r_value,p_value,std_err))
          #print('scipy coefficient of determination {}'.format(r_value**2))

      print('Done pruning, coefficient of determination {}'.format(r_value**2))


      #one_piece_x = [collapsed_x[0],collapsed_x[-1]]
      #one_piece_y = [h(collapsed_x[0]),h(collapsed_x[-1])]
      one_piece_x = [lgx[0],lgx[-1]]
      one_piece_y = [h(lgx[0]),h(lgx[-1])]
      print('one_piece_x       {}'.format(one_piece_x))
      print('one_piece_y       {}'.format(one_piece_y))

      one_piece_y_scipy = [slope_*lgx[0]+intercept_,slope_*lgx[-1]+intercept_]
      print('one_piece_y_scipy {}'.format(one_piece_y_scipy))

      one_piece_y = one_piece_y_scipy 
      if False:
        slopes = []
        for i in range(len(breaks)-1):
          print('searching for points between {} and {}'.format(breaks[i],breaks[i+1]))
          saved = []
          saved_y = []
          cnt = 0
          while cnt < 2:
            for j,xx in enumerate(x_hat):
              if breaks[i] < xx and xx < breaks[i+1] and y_hat[j] not in saved_y:
                saved.append((xx,y_hat[j]))
                saved_y.append(y_hat[j])
            cnt += 1
          if len(saved) >= 2:
            slopes.append(float((saved[1][1]-saved[0][1])/(saved[1][0]-saved[0][0])))
        label_ = 'n='+str(n)+', slopes='+str(slopes)
        print('slopes {}'.format(slopes))
      elif True:
        slope = float((one_piece_y[1]-one_piece_y[0])/(one_piece_x[1]-one_piece_x[0]))
        slope_data.append([n,slope])
        label_ = 'n='+str(n)+', slope='+str(slope)
      else:
        label_ = 'n='+str(n)

      #fp = open('collaped_points.csv','w')
      #for j,xx in enumerate(lgx):
      #  s = str(xx)+','+str(lgy[j])+'\n'
      #  fp.write(s)
      #fp.close()

      color = plot_colors[color_idx]
      line_type = plot_line_types[line_type_idx]
      marker_spec = color + 'o'
      line_spec = color + line_type

      if True:
        # normal scale
        ax.plot(lgx,lgy,marker_spec,markersize=3)
        ax.plot(one_piece_x,one_piece_y,line_spec,label=label_)
      else:
        # log-log scale
        pruned_x = [10**k for k in lgx]
        pruned_y = [10**k for k in lgy]      
        #m = slope_
        #b = intercept_
        m = float((one_piece_y[1]-one_piece_y[0])/(one_piece_x[1]-one_piece_x[0]))
        b = y_intercept(one_piece_x[0],one_piece_y[0],one_piece_x[1],one_piece_y[1])
        poly_fit_x = [10**k for k in lgx]
        poly_fit_y = [(10**b)*(k**m) for k in poly_fit_x]
        label_ = 'n='+str(n)+', y='+str(10**b)+' x^'+str(m)
        ax.loglog(pruned_x,pruned_y,marker_spec,markersize=3,basex=10,basey=10)
        ax.loglog(poly_fit_x,poly_fit_y,line_spec,label=label_)

      color_idx = (color_idx + 1) % len(plot_colors)
      line_type_idx = (line_type_idx + 1) % len(plot_line_types)

      #print("slope_data {}".format(slope_data))

  slope_data.sort(key = lambda x: x[0])
  with open('slope_data.csv','w') as fp:
    writer = csv.writer(fp)
    writer.writerows(slope_data)
  fp.close()
  if True:
    plt.xlabel('log(cache size)')
    plt.ylabel('log(cache misses)')
  else:
    plt.xlabel('cache size')
    plt.ylabel('cache misses')
  ax.legend(loc='lower right')
  t = 'LCS traceback, LRU, instance type: 0^k 1^k, plot of tradeoff between cache size and cache misses, one piece regression, pruned to have abs(r^2)>=0.999'
 
  plt.title(t)
  plt.show()

if False:
  data = [line.rstrip('\n').split(',') for line in open('slope_data.csv')]
  x = [float(k[0]) for k in data]
  y = [float(k[1]) for k in data]
  print('x {}'.format(x))
  print('y {}'.format(y))
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.plot(x,y,'bo',markersize=3)
  plt.xlabel('LCS Instance Size')
  plt.ylabel('Slope of regression line fitted to sweet spot points in cache size/cache misses tradeoff')
  plt.title('slope of one piece regression line as a function of input size for LCS traceback, LRU, instance type: 0^k 1^k')
  plt.show()

# plot 5
if plot_5:
  #results_path = './lcs_results_1_sm'
  #results_path = './lcs_results_2_sm'
  #results_path = './lcs_results'
  results_path = './lcs_binary_search'
  #results_path = './lcs_fixed_points'
  f = lambda x: x if len(x) > 0 else '0'
  d = os.listdir(results_path)
  d = sorted(d)
  fig = plt.figure()
  ax = fig.add_subplot(111)
  color_idx = 0
  line_type_idx = 0
  for new_field in d:
    new_list = [line.rstrip('\n').split(',') for line in open(results_path+'/'+new_field)]
    n = int(new_list[0][1][0:new_list[0][1].find('-')])
    #if True:
    #if n in {160}:
    #if n in {40,80,120,160,200,240}:
    if True and n>4:
      print('n = {}'.format(n))
      new_list = [[f(x[0]),f(x[1])] for x in new_list]
      x = [int(j) for j in [k[0] for k in new_list][1:]][0:-1]
      y = [int(j) for j in [k[1] for k in new_list][1:]][0:-1]
      collapsed_x = []
      collapsed_y = []
      for j,k in enumerate(x):
        collapsed_x.append(k)
        collapsed_y.append(y[j])
      x_dict = {}
      for j,k in enumerate(collapsed_x):
        x_dict[k] = collapsed_y[j]
      #ax.plot(x,y,color='blue',linewidth=1)
      y_dict = {}
      for k,v in x_dict.items():
        y_dict[v] = -1
      min_y_dict = {}
      y_list = list(y_dict.keys())
      sorted(y_list)
      highest_y = y_list[-1]
      print('highest y {}'.format(highest_y))
      low_y1 = y_list[0]
      print('low_y1 {}'.format(low_y1))
      low_y2 = y_list[1]
      print('low_y2 {}'.format(low_y2))
      low_y3 = y_list[2]
      print('low_y3 {}'.format(low_y3))
      collapsed = []
      selected = []
      for item in y_dict:
        if not(item==highest_y or item==low_y1 or item==low_y2 or item==low_y3):
          tmp = []
          for xval in collapsed_x:
            if x_dict[xval] == item:
              tmp.append(xval)
          for x_val in tmp:
            collapsed.append((min(tmp),item))
          min_y_dict[item] = min(tmp)
          selected.append((min(tmp),item))
      collapsed_x = []
      collapsed_y = []
      for g in collapsed:
        collapsed_x.append(g[0])
        collapsed_y.append(g[1])
      selected_x = []
      selected_y = []
      for g in selected:
        selected_x.append(g[0])
        selected_y.append(g[1])
      if True:
        chosen_x = collapsed_x
        chosen_y = collapsed_y
      else:
        chosen_x = selected_x
        chosen_y = selected_y
      lgx = [log(k,10) for k in chosen_x]
      lgy = [log(k,10) for k in chosen_y]

      # remove "last" sweet spot
      print('len lgx before removal {}'.format(len(lgx)))
      print('len lgy before removal {}'.format(len(lgy)))
      #max_times = 1 if n is not 40 else 2
      max_times = 0
      cnt = 0
      while cnt < max_times:
        lowest_x_indices = [i for i,xx in enumerate(lgx) if xx==min(lgx)]
        print('min lgx {}'.format(min(lgx)))
        print('lowest x indices {}'.format(lowest_x_indices))
        lgx = [k for i,k in enumerate(lgx) if i not in lowest_x_indices]
        lgy = [k for i,k in enumerate(lgy) if i not in lowest_x_indices]
        cnt += 1
      print('len lgx after removal {}'.format(len(lgx)))
      print('len lgy after removal {}'.format(len(lgy)))


      #p = np.polyfit(collapsed_x,collapsed_y,1)
      p = np.polyfit(lgx,lgy,1)
      h = np.poly1d(p)
      print('one piece p = {}'.format(p))

      slope_, intercept_, r_value, p_value, std_err = stats.linregress(lgx,lgy)
      print('scipy results {} {} {} {} {}'.format(slope_,intercept_,r_value,p_value,std_err))
      print('scipy coefficient of determination {}'.format(r_value**2))


      #(x_hat,y_hat,breaks) = do_piecewise_regression(collapsed_x,collapsed_y,2)
      #(x_hat,y_hat,breaks) = do_piecewise_regression(lgx,lgy,2)
      #print(collapsed_x[0])
      #print(log(collapsed_x[0]))

      # post-regression pruning - old way
      if False:
        max_times = 4
        cnt = 0
        while cnt < max_times:
          print('prune cnt {}'.format(cnt))
          x_median = calculate_median(lgx)
          far_right_indices = [i for i,xx in enumerate(lgx) if xx >= x_median]
          print('len far right indices {}'.format(len(far_right_indices)))
          removal_indices = [i for i,yy in enumerate(lgy) if i in far_right_indices and yy > h(lgx[i])]
          print('len removal indices {}'.format(len(removal_indices)))
          lgx = [k for i,k in enumerate(lgx) if i not in removal_indices]
          lgy = [k for i,k in enumerate(lgy) if i not in removal_indices]
          p = np.polyfit(lgx,lgy,1)
          h = np.poly1d(p)
          cnt += 1

      # post-regression pruning - new way
      highest_x = 0
      if False:
        while len(lgx) > 2:
          if abs(r_value**2) >= 0.999:
            break
          highest_x = max(lgx)
          remaining_indices = [i for i,xx in enumerate(lgx) if xx != highest_x]
          lgx = [k for i,k in enumerate(lgx) if i in remaining_indices]
          lgy = [k for i,k in enumerate(lgy) if i in remaining_indices]
          #print('removed {} points now there are {} {} points'.format(len(remaining_indices),len(lgx),len(lgy)))
          slope_, intercept_, r_value, p_value, std_err = stats.linregress(lgx,lgy)
          #print('scipy results {} {} {} {} {}'.format(slope,intercept,r_value,p_value,std_err))
          #print('scipy coefficient of determination {}'.format(r_value**2))

      # post_regression pruning - by function of input size
      alpha = 0
      if True:
        #alpha = get_best_prune_factor(lgx,lgy,n)
        alpha = 2
        remaining_indices = [i for i,xx in enumerate(lgx) if 10**xx < (alpha * n * sqrt(n))]
        lgx = [k for i,k in enumerate(lgx) if i in remaining_indices]
        lgy = [k for i,k in enumerate(lgy) if i in remaining_indices]
        slope_, intercept_, r_value, p_value, std_err = stats.linregress(lgx,lgy)

      highest_x = round(10**max(lgx))

      print('Done pruning, coefficient of determination {}'.format(r_value**2))

      #one_piece_x = [collapsed_x[0],collapsed_x[-1]]
      #one_piece_y = [h(collapsed_x[0]),h(collapsed_x[-1])]
      one_piece_x = [lgx[0],lgx[-1]]
      one_piece_y = [h(lgx[0]),h(lgx[-1])]
      print('one_piece_x {}'.format(one_piece_x))
      print('one_piece_y {}'.format(one_piece_y))
      one_piece_y_scipy = [slope_*lgx[0]+intercept_,slope_*lgx[-1]+intercept_]
      print('one_piece_y_scipy {}'.format(one_piece_y_scipy))

      one_piece_y = one_piece_y_scipy
      if False:
        slopes = []
        for i in range(len(breaks)-1):
          print('searching for points between {} and {}'.format(breaks[i],breaks[i+1]))
          saved = []
          saved_y = []
          cnt = 0
          while cnt < 2:
            for j,xx in enumerate(x_hat):
              if breaks[i] < xx and xx < breaks[i+1] and y_hat[j] not in saved_y:
                saved.append((xx,y_hat[j]))
                saved_y.append(y_hat[j])
            cnt += 1
          if len(saved) >= 2:
            slopes.append(float((saved[1][1]-saved[0][1])/(saved[1][0]-saved[0][0])))
        label_ = 'n='+str(n)+', slopes='+str(slopes)
        print('slopes {}'.format(slopes))
      elif True:
        label_ = 'n='+str(n)+', slope='+str(float((one_piece_y[1]-one_piece_y[0])/(one_piece_x[1]-one_piece_x[0])))+', r^2='+str(float(r_value**2))
      else:
        label_ = 'n='+str(n)

      m = float((one_piece_y[1]-one_piece_y[0])/(one_piece_x[1]-one_piece_x[0]))
      b = y_intercept(one_piece_x[0],one_piece_y[0],one_piece_x[1],one_piece_y[1])
      pruned_x = [10**k for k in lgx]
      pruned_y = [10**k for k in lgy]
      poly_fit_x = [10**k for k in lgx]
      poly_fit_y = [(10**b)*(k**m) for k in poly_fit_x]
      label_ = 'n='+str(n)+', y='+str(10**b)+' x^'+str(m)+', r^2='+str(float(r_value**2))+', alpha='+str(float(alpha))+', max(x)='+str(highest_x)

      color = plot_colors[color_idx]
      line_type = plot_line_types[line_type_idx]
      marker_spec = color + 'o'
      line_spec = color + line_type

      # log-log scale
      ax.loglog(pruned_x,pruned_y,marker_spec,markersize=3,basex=10,basey=10)
      ax.loglog(poly_fit_x,poly_fit_y,line_spec,label=label_)


      # normal scale
      #ax.plot(collapsed_x,collapsed_y,marker_spec,markersize=3)
      #ax.plot(one_piece_x,one_piece_y,line_spec,label=label_)
      #ax.plot(lgx,lgy,marker_spec,markersize=3)
      #ax.plot(lgx,h(lgx),line_spec,label=label_)
      #ax.plot(x_hat,y_hat,line_spec,label=label_)
      #ax.plot(collapsed_x,h(collapsed_x),line_spec,label=label_)

      color_idx = (color_idx + 1) % len(plot_colors)
      line_type_idx = (line_type_idx + 1) % len(plot_line_types)

  plt.xlabel('cache size')
  plt.ylabel('cache misses')
  #ax.legend(loc='upper right')
  ax.legend(loc='lower right')
  #t = 'LCS traceback, LRU, instance type: 0^k 1^k, plot of tradeoff between cache size and cache misses, one piece regression, pruned to have abs(r^2)>=0.999\n'
  t = 'LCS traceback, LRU, instance type: 0^k 1^k, plot of tradeoff between cache size and cache misses, one piece regression, pruned using cutoff as function of N\n'
  #t += 'cache sizes are measured at evenly spaced intervals spaced N apart, where N is the instance size in question, note these are not sweet spots'
  t += 'cache sizes are sweet spots found by binary search\n'
  t += 'cutoff cache size for instance size N = alpha * N * sqrt(N)'
 
  plt.title(t)
  plt.show()




exit()
# OLD
results_path = './lcs_results'
f = lambda x: x if len(x) > 0 else '0'
d = os.listdir(results_path)
lists = []
cnt = 1
fig = plt.figure()
ax = fig.add_subplot(111)
for new_field in d:
  new_list = [line.rstrip('\n').split(',') for line in open(results_path+'/'+new_field)]
  n = int(new_list[0][1][0:new_list[0][1].find('-')])
  #print(new_list[0][1])

  if new_list[0][1] == '50-test-000-111.lcs':
    found = True
  else:
    found = False
  new_list = [[f(x[0]),f(x[1])] for x in new_list]
  #print(new_list)
  x = [int(j) for j in [k[0] for k in new_list][1:]][0:-1]
  y = [int(j) for j in [k[1] for k in new_list][1:]][0:-1]
  if found == True:
    selected_x = []
    selected_y = []
    for j,k in enumerate(x):
      if (k>=83 and k<=872) or True:
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
    lgx = [log(k) for k in sweet_x]
    lgy = [log(k) for k in sweet_y]
    lgz = np.polyfit(np.array(lgx),np.array(lgy),2)
    print(lgz)
    lgp = np.poly1d(lgz)
    z = np.polyfit(x,y,1)
    p = np.poly1d(z)

  #print(x)
  #print(y)
  ax.plot(x,y,color='blue',linewidth=1)
  cnt += 1
  #if cnt > 2:
  #  break
#ax.plot([62,900],[p(62),p(900)],color='red',linewidth=4)
#ax.plot([62,900],[lgp(62),lgp(900)],color='green',linewidth=4)
#plt.title('N = 30, 406 instances + interpolation of worst case, a='+str(z[0])+', b='+str(z[1])+', using log values a='+str(lgz[0])+', b='+str(lgz[1]))
#plt.xlabel('cache size')
#plt.ylabel('cache misses')
#plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)
#ax.plot(lgx,lgy,color='blue',linewidth=1)
ax.scatter(lgx,lgy,color='green')
#ax.plot([log(62),log(872)],[lgp(log(62)),lgp(log(872))],color='red',linewidth=1)
ax.plot(lgx,lgp(lgx),color='red',linewidth=1)
plt.title('linear regression log(y) = '+str(lgz[0])+'log(x) + '+str(lgz[1]))
plt.xlabel('log(cache size)')
plt.ylabel('log(cache misses)')
plt.show()

do_piecewise_regression(lgx,lgy)

do_piecewise_linear(lgx, lgy)
