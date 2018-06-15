import matplotlib.pyplot as plt
x = range(5, 20, 5)
SSE = [1, 3, 5]
plt.xlabel('k')
plt.ylabel('SSE')
plt.plot(x, SSE, 'o-')
plt.show()