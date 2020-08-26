# Usage: python plot_tspr.py <folder>


import matplotlib.pyplot as plt
import os, sys


folder = sys.argv[1]
d = os.listdir(folder)
for j,ff in enumerate(d):
  print('{}:{}'.format(j,ff))
idx = int(input("Choose file by entering number: "))
fname = folder + d[idx]
print('chosen: {}'.format(fname))
lines = [line.rstrip('\n') for line in open(fname)]
for j,line in enumerate(lines):
  #print(line)
  if line.find('NAME') is not -1:
    print('found NAME -->{}<--'.format(line))
  if line.find('TYPE') is not -1:
    print('found TYPE -->{}<--'.format(line))
  if line.find('COMMENT') is not -1:
    print('found COOMENT -->{}<--'.format(line))
  if line.find('DATA_POINTS') is not -1:
    data_x = []
    data_y = []
    print('found DATA_POINTS -->{}<--'.format(line))
    for k in range(1,int(line.split(' ')[1])+1):
      print('point {}'.format(lines[j+k]))
      data_x.append(int(lines[j+k].split(' ')[0]))
      data_y.append(int(lines[j+k].split(' ')[1]))
  if line.find('PORTALS') is not -1:
    portal_x = []
    portal_y = []
    print('found PORTALS -->{}<--'.format(line))
    for k in range(1,int(line.split(' ')[1])+1):
      print('point {}'.format(lines[j+k]))
      portal_x.append(int(lines[j+k].split(' ')[0]))
      portal_y.append(int(lines[j+k].split(' ')[1]))
  if line.find('PARTITIONS') is not -1:
    partitions = []
    print('found PARTITIONS -->{}<--'.format(line))
    for k in range(1,int(line.split(' ')[1])+1):
      print('partition {}'.format(lines[j+k]))
      x1 = int(lines[j+k].split(' ')[0])
      y1 = int(lines[j+k].split(' ')[1])
      x2 = int(lines[j+k].split(' ')[2])
      y2 = int(lines[j+k].split(' ')[3])
      partitions.append((x1,y1,x2,y2))
  if line.find('ARORA_PATH') is not -1:
    arora_x = []
    arora_y = []
    print('found ARORA_PATH -->{}<--'.format(line))
    for k in range(1,int(line.split(' ')[1])+1):
      print('arora point {}'.format(lines[j+k]))
      arora_x.append(int(lines[j+k].split(' ')[0]))
      arora_y.append(int(lines[j+k].split(' ')[1]))
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(data_x,data_y,'bo')
ax.plot(portal_x,portal_y,'ro')
for p in partitions:
  ax.plot([p[0],p[2]],[p[1],p[1]],'g')
  ax.plot([p[0],p[2]],[p[3],p[3]],'g')
  ax.plot([p[0],p[0]],[p[1],p[3]],'g')
  ax.plot([p[2],p[2]],[p[1],p[3]],'g')
ax.plot(arora_x,arora_y,'c')
ax.plot([arora_x[0],arora_x[-1]],[arora_y[0],arora_y[-1]],'c')
plt.show()
