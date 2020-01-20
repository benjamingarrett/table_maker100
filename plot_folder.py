import csv,itertools,os,sys,re
import matplotlib.pyplot as plt

plot_line_types=['-','--','-.',':']
plot_colors=['b','g','r','c','m','y','k']
lists=sorted([[ln.rstrip('\n').split(',') for ln in open(sys.argv[1]+'/'+fn)] for fn in os.listdir(sys.argv[1]) if 'csv' in fn and fn!='m.csv'],key=lambda k:(int(k[1][1]),k[0][1]))
fig=plt.figure()
ax=fig.add_subplot(111)
color_idx=0
line_type_idx=0
for item in lists:
  print(item)
  label_=[k[1] for k in item if 'COMMENT' in k[0]]
  print(sys.argv[2])
  print(label_)
  #if True:
  #if bool(re.search(sys.argv[2]+'\Z',label_[0]))==True:
  #if bool(re.search(sys.argv[2],label_[0]))==True:a
  if bool(re.search('_100',label_[0]))==True or bool(re.search('_200',label_[0]))==True or bool(re.search('_300',label_[0]))==True or bool(re.search('_400',label_[0]))==True or bool(re.search('_500',label_[0]))==True:
    x=[int(k[0]) for k in item if 'COMMENT' not in k[0] and 'SORT_BY' not in k[0]]
    y=[int(k[1]) for k in item if 'COMMENT' not in k[0] and 'SORT_BY' not in k[0]]
    print(x)
    print(y)
    color=plot_colors[color_idx]
    line_type=plot_line_types[line_type_idx]
    line_spec=color+line_type
    ax.plot(x,y,line_spec,linewidth=1,label=label_)
    color_idx=(color_idx+1)%len(plot_colors)
    line_type_idx=(line_type_idx+1)%len(plot_line_types)
plt.xlabel('cache size')
plt.ylabel('cache misses')
ax.legend(loc='upper right')
plt.title(sys.argv[1])
plt.show()
