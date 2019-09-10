import matplotlib.pyplot as plt
import numpy as np
from math import log
from numpy import interp

f = lambda x,c,d,e,g,h: c/(g*(x-e+1)**h)+d
#f = lambda x,c: c/log(x**0.5)
x = [62,  92,  123, 157, 181, 185, 206, 219, 249, 404]
y = [8370,8311,6045,4723,4243,4185,4018,3873,3739,2878]
cx = [xi for xi in range(min(x),max(x)+1)]
cp = max(y)
dp = -14500
ep = min(x)
gp = 0.5
hp = 0.1
cy = [f(xi,cp,dp,ep,gp,hp) for xi in cx]
#cy = [f(xi,max(y)) for xi in cx]
#print(cx)
#print(cy)
s = 'Conjecture: f(x)='+str(cp)+'/('+str(gp)+"*(x-"+str(ep)+")^"+str(hp)+")"

lgx = [log(k) for k in x]
lgy = [log(k) for k in y]
lgz = np.polyfit(np.array(lgx),np.array(lgy),1)

z = np.polyfit(np.array(x),np.array(y),1)
#print(lgz)
print('polyfit {}'.format(z))
exit()

plt.title(s)
p1 = plt.plot(x,y,'r')
p2 = plt.plot(cx,cy,'b')
#p3 = plt.plot(x,yy,'g')
plt.setp(p1)
plt.setp(p2)
#plt.setp(p3)
plt.legend(('data','conjecture','linear regression'),loc='upper right')
plt.show()
