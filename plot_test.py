import numpy as np
import matplotlib.pyplot as plt
from math import e,log

x = [4.1,6.5,12.6,25.5,29.8,38.6,46,52.8,59.6,66.3,74.7]
y = [2.2,4.5,10.4,23.1,27.9,36.8,44.3,50.7,57.5,64.1,72.6]

sx = [100*k for k in x]
sy = [100*k for k in y]

lgx = [log(k,10) for k in sx]
lgy = [log(k,10) for k in sy]

p = np.polyfit(sx,sy,1)
print('p {}'.format(p))
g = np.poly1d(p)

q = np.polyfit(lgx,lgy,1)
print('q {}'.format(q))
h = np.poly1d(q)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(sx,sy,'bo')
ax.plot([sx[0],sx[-1]],[g(sx[0]),g(sx[-1])],'r--')
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.loglog(lgx,lgy,'bo')
ax.loglog([lgx[0],lgx[-1]],[h(lgx[0]),h(lgx[-1])],'r--')
plt.show()
