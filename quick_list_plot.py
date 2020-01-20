import math
import matplotlib.pyplot as plt
import sys

y=[int(k) for k in [line.rstrip('\n').split(',') for line in open(sys.argv[1])][0]][0:260]
x=[k for k in range(1,len(y)+1)]
col=[(xx,y[i]) for i,xx in enumerate(x)]
with open('m_column_2019_11_06-20_39_59.csv','w') as fp:
  for k in col:
    fp.write(str(k[0])+','+str(k[1])+'\n')
fig=plt.figure()
ax=fig.add_subplot(111)
k=1
while k<len(y):
  if math.log(k,2)%1==0:
    ax.plot([k,k],[min(y),max(y)],color='blue')
  k+=1
ax.plot(x,y,color='red')
plt.xlabel('problem size, n, where the problem is to compute F(n)')
plt.ylabel('cache misses using LRU, cache size = 4')
t = 'Fibonacci version 2a, LRU, cache size = 4\n'
t+= 'Plot of cache misses as a function of problem size\n'
t+= 'Vertical lines at 2^k'
plt.title(t)
plt.show()
