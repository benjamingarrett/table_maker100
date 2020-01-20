import csv,os,sys,matplotlib.pyplot as plt
from math import log
import numpy as np
from scipy import stats


lists=sorted([[ln.rstrip('\n').split(',') for ln in open(sys.argv[1]+'/'+fn)] for fn in os.listdir(sys.argv[1]) if 'csv' in fn and fn != 'm.csv'],key=lambda k:(int(k[1][1]),k[0][1]))
x=[j[0] for j in list(filter(lambda u:len(u)>0,[[int(k[1]) for k in g if k[0]=='SORT_BY'] for g in lists]))]
y=[j[0] for j in list(filter(lambda u:len(u)>0,[[int(k[1]) for k in g if k[0]==sys.argv[2]] for g in lists]))]
print(x)
print(y)
lgx=[log(k,10) for k in x]
lgy=[log(k,10) for k in y]
lgy=y
h=np.poly1d(np.polyfit(lgx,lgy,1))
m=float((h(lgy[-1])-h(lgy[0]))/(lgx[-1]-lgx[0]))
b=h(lgy[0])-(h(lgy[-1])-h(lgy[0]))/(lgx[-1]-lgx[0])*lgx[0]
slope_, intercept_, r_value, p_value, std_err = stats.linregress(lgx,lgy)
print('scipy results {} {} {} {} {}'.format(slope_,intercept_,r_value,p_value,std_err))
print('scipy coefficient of determination {}'.format(r_value**2))
print('m {}  b {}'.format(m,b))
m=slope_
#py=[(10**b)*(k**m) for k in x]
py=y
fig=plt.figure()
ax=fig.add_subplot(111)
#ax.plot(x,y)
ax.loglog(x,y,'bo',markersize=1)
ax.loglog(x,py,'r-')
plt.show()
