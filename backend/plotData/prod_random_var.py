import numpy as np
import matplotlib.pyplot as plt

n_samples = 10**5
m= 100

x1 = np.random.randint(low = 1, high = m, size = n_samples)
y1 = np.random.randint(low = 1, high = m, size = n_samples)
x2 = np.random.randint(low = 1, high = m**2, size = n_samples)

# x1 = np.arange(start = 1, stop = m)
# y1 = np.arange(start = 1, stop = m)
# x2 = np.arange(start = 1, stop = m**2)


Z1 = x1*y1
hist1 = np.hstack(Z1)

Z2 = x1*y1 + x2
hist2 = np.hstack(Z2)

fig = plt.figure()

plt.subplot(2,2,1)
plt.hist(hist1, bins = 'auto')
plt.title("x1*y1 with binning")
plt.ylabel("Number of samples")

plt.subplot(2,2,2)
plt.hist(hist1, bins = m**2)
plt.title("x1*y1")
plt.ylabel("Number of samples")

plt.subplot(2,2,3)
plt.hist(hist2, bins = 'auto')
plt.title("x1*y1 + x2 with binning")
plt.ylabel("Number of samples")

plt.subplot(2,2,4)
plt.hist(hist2, bins = m**2)
plt.title("x1*y1 + x2")
plt.ylabel("Number of samples")

plt.suptitle("m = " + str(m))
plt.show()