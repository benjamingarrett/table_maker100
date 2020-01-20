import matplotlib.pyplot as plt
import sys


lists=[ln.rstrip('\n').split(',') for ln in open(sys.argv[1])]
x=[int(k[0]) for k in lists]
y=[float(k[int(sys.argv[2])]) for k in lists]
fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot(x,y)
plt.xlabel('problem size, n')
plt.ylabel('minimum cache misses')
plt.title('Fib 1a')
plt.show()
