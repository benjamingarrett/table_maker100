import matplotlib.pyplot as plt

list1 = [[1,1],[2,4],[3,9],[4,16]]
list2 = [[1,2],[2,8],[3,18],[4,32]]
plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'ro')
plt.plot([1, 2, 3, 4], [2, 8, 18, 32], 'bo')
plt.axis([0, 60, 0, 40])
plt.show()
