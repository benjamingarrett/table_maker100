# Usage: python plot_folder.py <folder> <title> <x_axis> <y_axis>


import csv,itertools,os,sys,re
import matplotlib.pyplot as plt


def do_plot(folder, title, x_axis, y_axis, legend_location='lower_right'):
  print('do_plot: {} {} {} {}'.format(folder, title, x_axis, y_axis))
  plot_line_types = ['-','--','-.',':']
  plot_colors = ['b','g','r','c','m','y','k']
  locations = {'lower_right': 'lower right', 'lower_left': 'lower left', 'upper_right': 'upper right', 'upper_left': 'upper left'}
  lists = []
  for fn in os.listdir(folder):
    if not os.path.isdir(folder+'/'+fn) and not (folder+'/'+fn).endswith('.log') and (folder+'/'+fn).endswith('.csv'): 
      lists.append((fn, [ln.rstrip('\n').split(',') for ln in open(folder+'/'+fn)]))
  #lists = sorted([[ln.rstrip('\n').split(',') for ln in open(folder+'/'+fn)] for fn in os.listdir(folder)], key=lambda k:(int(k[1][1]),k[0][1]))
  #print(lists)
  if len(lists) == 0:
    print('No results found!')
    exit()
  fig = plt.figure()
  ax = fig.add_subplot(111)
  color_idx = 0
  line_type_idx = 0
  for item in lists:
    print('item ->{}<-'.format(item))
    #label_ = [k[1] for k in item if 'COMMENT' in k[0]]
    label_ = [k[1] for k in item[1] if 'LABEL' in k[0]][0]
    if len(label_) == 0:
      label_ = [k[1] for k in item[1] if 'COMMENT' in k[0]][0]
      if len(label_) == 0:
        label_ = item
    print(label_)
    if True:
      x = [float(k[0]) for k in item[1] if 'COMMENT' not in k[0] and 'SORT_BY' not in k[0] and 'LABEL' not in k[0] and 'problem_size' not in k[0]]
      y = [float(k[1]) for k in item[1] if 'COMMENT' not in k[0] and 'SORT_BY' not in k[0] and 'LABEL' not in k[0] and 'cache_misses' not in k[1]]
      print(x)
      print(y)
      color = plot_colors[color_idx]
      line_type = plot_line_types[line_type_idx]
      line_spec = color+line_type
      ax.plot(x, y, line_spec, linewidth=1, label=label_)
      #ax.loglog(x, y, line_spec, basex=2, basey=2, linewidth=1, label=label_)
      #ax.plot(x, y, 'o', label=label_)
      color_idx = (color_idx+1)%len(plot_colors)
      line_type_idx = (line_type_idx+1)%len(plot_line_types)
  plt.xlabel(x_axis)
  plt.ylabel(y_axis)
  ax.legend(loc=locations[legend_location.rstrip()])
  plt.title(title)
  plt.show()


if __name__ == '__main__':
  '''
  Note: these files contain title, x-axis, y-axis, and legend location and should be keep in 
  a separate folder from the data itself
  '''
  if len(sys.argv) == 1:
    print('plot_folder.py: Error - provide at least the folder location')
    exit(1)
  if len(sys.argv) == 2:
    with open(os.path.join(sys.argv[1], 'metadata/title')) as fp:
      title = fp.read()
    with open(os.path.join(sys.argv[1], 'metadata/x_axis')) as fp:
      x_axis = fp.read()
    with open(os.path.join(sys.argv[1], 'metadata/y_axis')) as fp:
      y_axis = fp.read()
    with open(os.path.join(sys.argv[1], 'metadata/legend_location')) as fp:
      legend_location = fp.read()
  else:
    with open(sys.argv[2]) as fp:
      title = fp.read()
    with open(sys.argv[3]) as fp:
      x_axis = fp.read()   
    with open(sys.argv[4]) as fp:
      y_axis = fp.read()
    with open(sys.argv[5]) as fp:
      legend_location = fp.read().rstrip()
  do_plot(sys.argv[1], title, x_axis, y_axis, legend_location)
