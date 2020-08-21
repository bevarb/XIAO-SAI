import matplotlib.pyplot as plt
import numpy as np
fig,ax = plt.subplots()
for key, spine in ax.spines.items():
    if key == "right" or key == "top":
        spine.set_visible(False)
X = np.arange(0, 1, 0.01)
Y = 0.391 * X + 0.061
plt.plot(X, Y)
plt.text(0, 0.391 + 0.061, "y = 0.391x + 0.061", fontsize=15)
plt.show()