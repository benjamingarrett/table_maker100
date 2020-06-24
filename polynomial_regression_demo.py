import matplotlib.pyplot as plt
import numpy
from sklearn.metrics import r2_score

x = [1,2,3,5,6,7,8,9,10,12,13,14,15,16,18,19,21,22]
y = [100,90,80,60,60,55,60,65,70,70,75,76,78,79,90,99,99,100]
mymodel = numpy.poly1d(numpy.polyfit(x, y, 3))
myline = numpy.linspace(1, 22, 100)
coeffs = []
p_str = ''
j = 0
while j < mymodel.o:
  coeffs.append(mymodel.c[j])
  exp = ' x'
  if mymodel.o-j > 1:
    exp += '^{}'.format(mymodel.o-j)
  if mymodel.c[j+1] >= 0:
    p_str += '{} {} +'.format(mymodel.c[j], exp)
  else:
    p_str += '{} {} '.format(mymodel.c[j], exp)
  j += 1
p_str += '{}'.format(mymodel.c[mymodel.o])
print(mymodel.o)
print(coeffs)
print(mymodel.c)
print(p_str)

plt.scatter(x, y)
plt.plot(myline, mymodel(myline))
t = 'Polynomial Regression Demo\n'
t+= 'polynomial: {}\n'.format(p_str)
t+= 'r2 score: {}'.format(r2_score(y, mymodel(x)))
plt.title(t)
plt.show()
