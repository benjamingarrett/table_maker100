import matplotlib.pyplot as plt
import math
import sys

f=lambda u:u**4-u**3-1
g=lambda u:0
#x=[20,40,80,160,320,640,1280]
#y=[1.6705
x=[k for k in range(-1000,1001)]
y1=[f(k) for k in x]
y2=[g(k) for k in x]
fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot(x,y1,color='lightblue')
ax.plot(x,y2,color='red')
plt.show()
