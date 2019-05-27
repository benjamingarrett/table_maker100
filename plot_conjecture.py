import csv, itertools, os
import numpy as np
import matplotlib.pyplot as plt
import math

e = lambda p,q: q*p**2
f = lambda p,q: p**q
#f = lambda p,q: q*p**2
g = lambda p,q: q**p

k = 2.88532
h = 1.88
i = 58
x = []
y = []
with open('plotting_data.csv') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  for row in reader:
    print(row)
    x.append(int(row[0]))
    y.append(int(row[1]))
print(x)
print(y)
cx = x
cy = [f(u,k) for u in x]
print(cx)
print(cy)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x, y, color='lightblue', linewidth=3)
ax.plot(cx, cy, color='red', linewidth=3)
#cx1 = x
#cy1 = [g(u,h) for u in x]
#ax.plot(cx1, cy1, color='green', linewidth=3)
#cx2 = x
#cy2 = [e(u,i) for u in x]
#ax.plot(cx2, cy2, color='orange', linewidth=3)
plt.savefig('version_2a_data_and_conjecture.png')
plt.show()
quit()
t = np.arange(0.01, 10.0, 0.01)
data1 = np.exp(t)
data2 = np.sin(2 * np.pi * t)
data1 = (t+10) * 2
data2 = (t+1000) * 3
#print(data1)
#print(data2)
fig, ax1 = plt.subplots()
color = 'tab:red'
ax1.set_xlabel('time (s)')
ax1.set_ylabel('exp', color=color)
ax1.plot(t, data1, color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('sin', color=color)
ax2.plot(t, data2, color=color)
ax2.tick_params(axis='y', labelcolor=color)
fig.tight_layout()
plt.show()

