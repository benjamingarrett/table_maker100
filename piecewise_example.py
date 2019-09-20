import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import statsmodels.formula.api as smf

# plot inline rather than pop out
#%matplotlib inline
# change the plot size, default is (6, 4) which is a little small
plt.rcParams['figure.figsize'] = (16, 12)

np.random.seed(9999)
x = np.random.normal(0, 1, 1000) * 10
y = np.where(x < -15, -2 * x + 3 , np.where(x < 10, x + 48, -4 * x + 98)) + np.random.normal(0, 3, 1000)
plt.scatter(x, y, s = 5, color = u'b', marker = '.', label = 'scatter plt')
plt.show()


# linear regression
#f1 = smf.ols(formula = 'y ~ x', data = dtest).fit()
#dtest['f1_pred'] = f1.predict()
# print f1.summary()

fig = plt.figure()
fig.patch.set_alpha = 0.5

ax = fig.add_subplot(111)
ax.plot(x, y, linestyle = '', color = 'k', linewidth = 0.25, markeredgecolor='none', marker = '.', label = r'scatter plot')
ax.plot(dtest.x, dtest.f1_pred, color = 'blue', linestyle = '-', linewidth = 1, markeredgecolor='none', marker = '', label = r'lin-reg')
ax.annotate('$y = 44.25 - 0.0645 x$', (10, 43), xytext = (0.5, 0.4), fontsize = 20, textcoords = 'axes fraction',  arrowprops = dict(facecolor = 'grey', color = 'grey'))
plt.show()



# piecewise linear data prepare
x1 = np.where(x > -15, x + 15, 0)
x2 = np.where(x > 10, x - 10, 0)
dtest = pd.DataFrame([y, x, x1, x2]).T
dtest.columns = ['y', 'x', 'x1', 'x2']

# piecewise linear regression
f2 = smf.ols(formula = 'y ~ x + x1 + x2', data = dtest).fit()
dtest['f2_pred'] = f2.predict()
# print f2.summary()

dtest.sort('x', inplace = True)

fig = plt.figure(figsize = (16, 12))

ax = fig.add_subplot(111)

ax.plot(x, y, linestyle = '', color = 'k', linewidth = 0.25, markeredgecolor='none', marker = '.', label = r'scatter plot')
ax.plot(dtest.x, dtest.f2_pred, color = 'b', linestyle = '-', linewidth = 2, markeredgecolor='none', marker = '', label = r'pw-reg')
ax.set_ylabel('Y', labelpad = 6)

# pd.DataFrame([x, f2_pred]).to_excel(r'c:\test.xlsx')

ax.annotate('-2x + 3', (-25, 53), xytext = (-.95, 0.4), fontsize = 20, textcoords = 'axes fraction', arrowprops = dict(facecolor = 'grey', color = 'grey'))
ax.annotate('x + 48', (0, 48), xytext = (0.35, 0.9), fontsize = 20, textcoords = 'axes fraction', arrowprops = dict(facecolor = 'grey', color = 'grey'))
ax.annotate('-4x + 98', (18, 20), xytext = (0.7, 0.2), fontsize = 20, textcoords = 'axes fraction', arrowprops = dict(facecolor = 'grey', color = 'grey'))


plt.legend(loc = 3, ncol = 1)

plt.show()

