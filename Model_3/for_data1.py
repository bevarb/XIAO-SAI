import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Model_3.plot.plot_RS import plot_RS, plot_COD_RS
from scipy import optimize

data01 = pd.read_csv("data/data01.csv")
data1 = np.zeros([15 * 3, 3], dtype=np.float)
for i in range(len(data01)):
    t = data01.loc[i]["t"]
    cod = data01.loc[i]["COD"]
    rs = data01.loc[i]["RS"]
    data1[i, :] = np.array([t, cod, rs]).astype(np.float)
data1 = np.array(sorted(data1.tolist(), key=lambda x: x[1]))
print(data1)
def __calculate_rr__(x, y, total):
    def f_1(x, A, B):
        return A * x + B
    a, b = optimize.curve_fit(f_1, x, y)[0]
    y_tar = x * a +b
    y_mean = np.ones(total) * (np.sum(y) / total)
    RSS = np.sum(np.square(y - y_tar))
    TSS = np.sum(np.square(y - y_mean))
    rr = round(1 - RSS / TSS, 3)
    return a, b, rr
a, b, rr = __calculate_rr__(data1[:, 2], data1[:, 1], len(data1))
plot_COD_RS(data1, a, b, rr)
