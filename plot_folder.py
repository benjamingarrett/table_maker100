# Usage: python plot_folder.py <folder> <title> <x_axis> <y_axis>


import csv,itertools,os,sys,re
import matplotlib.pyplot as plt


def do_plot(folder, title, x_axis, y_axis):
  print('do_plot: {} {} {} {}'.format(folder, title, x_axis, y_axis))
  plot_line_types = ['-','--','-.',':']
  plot_colors = ['b','g','r','c','m','y','k']
  lists = []
  for fn in os.listdir(folder):
    if not os.path.isdir(folder+'/'+fn) and not (folder+'/'+fn).endswith('.log'): 
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
    print(item)
    #label_ = [k[1] for k in item if 'COMMENT' in k[0]]
    label_ = item[0]
    if len(label_) == 0:
      label_ = item
    print(label_)
    if True:
      x = [int(k[0]) for k in item[1] if 'COMMENT' not in k[0] and 'SORT_BY' not in k[0] and 'problem_size' not in k[0]]
      y = [int(k[1]) for k in item[1] if 'COMMENT' not in k[0] and 'SORT_BY' not in k[0] and 'cache_misses' not in k[1]]
      print(x)
      print(y)
      color = plot_colors[color_idx]
      line_type = plot_line_types[line_type_idx]
      line_spec = color+line_type
      ax.plot(x, y, line_spec, linewidth=1, label=label_)
      #ax.plot(x, y, ',', label=label_)
      color_idx = (color_idx+1)%len(plot_colors)
      line_type_idx = (line_type_idx+1)%len(plot_line_types)
  plt.xlabel(x_axis)
  plt.ylabel(y_axis)
  ax.legend(loc='lower right')
  plt.title(title)
  plt.show()


if __name__ == '__main__':
  do_plot(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
