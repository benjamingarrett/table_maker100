import matplotlib.pyplot as plt

#x = list(range(100))
#y = list(range(20,120))
x = [0,100]
y = [20,119]
print(x)
print(y)
#plt.plot(x,y)
plt.loglog(x,y)
plt.show()
exit()





x = []
y = []
with open('opt_misses.csv') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')
  for row in reader:
    print(row)
    x.append(int(row[0]))
    y.append(int(row[1]))
print(x)
print(y)
cx = x
cy = [math.ceil(2*math.log2(u))+1 for u in x]
print(cx)
print(cy)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x, y, color='lightblue', linewidth=3)
ax.plot(cx, cy, color='red', linewidth=3)
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
