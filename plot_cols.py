# Usage: python plot_cols.py <csv_file> <column_number>
# Description: x-axis is first column, chosen column is y-axis

import matplotlib.pyplot as plt
import sys

lists=[ln.rstrip('\n').split(',') for ln in open(sys.argv[1])]
if len(sys.argv) >= 3:
  col=int(sys.argv[2])
else:
  col=1
x=[int(k[0]) for k in lists]
y=[float(k[col]) for k in lists]
fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot(x,y)
plt.xlabel('problem size, n')
plt.ylabel('minimum cache misses')
plt.title('Fib 1a')
plt.show()
