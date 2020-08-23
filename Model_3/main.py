import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Model_3.plot.plot_RS import plot_RS, plot_v, plot_fit_v, plot_fitted
from scipy import optimize
import scipy.interpolate as spi

def get_spi(new_x, X, Y, k):
    ipo3 = spi.splrep(X, Y, k=k)
    iy3 = spi.splev(new_x, ipo3)
    return iy3

data02 = pd.read_csv("data/data02.csv")
# 获得原始数据
data2 = np.zeros([3, 16, 4], dtype=np.float)
for i in range(len(data02)):
    id = int(data02.loc[i]["id"] - 1)
    t = data02.loc[i]["t"]
    cod = data02.loc[i]["COD"]
    rs = data02.loc[i]["RS"]
    p = data02.loc[i]["P"]
    data2[id, i % 16, :] = np.array([t, cod, rs, p]).astype(np.float)

# 获得插值的速度数据
new_x = np.arange(0, 100, 1)
new_y = np.zeros([3, 100, 4], dtype=np.float)
for i in range(3):
    if i !=3:
        iy3_cod = get_spi(new_x, data2[i, :, 0], data2[i, :, 1], 3)
        iy3_rs = get_spi(new_x, data2[i, :, 0], data2[i, :, 2], 3)
        iy3_p = get_spi(new_x, data2[i, :, 0], data2[i, :, 3], 3)
        new_y[i, :, 0] = new_x
        new_y[i, :, 1] = iy3_cod
        new_y[i, :, 2] = iy3_rs
        new_y[i, :, 3] = iy3_p

# plot_v(new_x, new_y, 1)

# 获得速度数据
v_data = np.zeros([3, 100, 4], dtype=np.float)
for i in range(3):
    for j in range(1, 100):
        dt = new_y[i, j, 0] - new_y[i, j - 1, 0]
        dc = new_y[i, j, 1] - new_y[i, j - 1, 1]
        ds = new_y[i, j, 2] - new_y[i, j - 1, 2]
        dp = new_y[i, j, 3] - new_y[i, j - 1, 3]
        v_data[i, j, :] = np.array([new_y[i, j, 0], dc/dt, ds/dt, dp/dt]).astype(np.float)
    v_data[i, 0, :] = v_data[i, 1, :]
# for i in range(3):
#     if i !=3:
#         iy3_cod = get_spi(new_x, v_data[i, :, 0], v_data[i, :, 1], 3)
#         iy3_rs = get_spi(new_x, v_data[i, :, 0], v_data[i, :, 2], 3)
#         iy3_p = get_spi(new_x, v_data[i, :, 0], v_data[i, :, 3], 3)
#         new_y[i, :, 0] = iy3_cod
#         new_y[i, :, 1] = iy3_rs
#         new_y[i, :, 2] = iy3_p
#     else:
#         x1 = np.arange(5, 80, 1)
#         x2 = np.arange(80, 100, 1)
#         iy3_cod1 = get_spi(x1, v_data[i, 0:14, 0], v_data[i, 0:14, 1], 3)
#         iy3_rs1 = get_spi(x1, v_data[i, 0:14, 0], v_data[i, 0:14, 2], 3)
#         iy3_p1 = get_spi(x1, v_data[i, 0:14, 0], v_data[i, 0:14, 3], 3)
#         new_y[i, 0:75, 0] = iy3_cod1
#         new_y[i, 0:75, 1] = iy3_rs1
#         new_y[i, 0:75, 2] = iy3_p1
#         iy3_cod2 = get_spi(x2, v_data[i, 13:15, 0], v_data[i, 13:15, 1], 1)
#         iy3_rs2 = get_spi(x2, v_data[i, 13:15, 0], v_data[i, 13:15, 2], 1)
#         iy3_p2 = get_spi(x2, v_data[i, 13:15, 0], v_data[i, 13:15, 3], 1)
#         new_y[i, 75:, 0] = iy3_cod2
#         new_y[i, 75:, 1] = iy3_rs2
#         new_y[i, 75:, 2] = iy3_p2
#
# plot_v(new_x, v_data, 0)

def get_fit_y(data, flag, new_y):
    def __calculate_rr__(x, y):
        def f_1(x, A, B, C, a, b, c, d):
            return A * x[:, 1] + B * x[:, 2] + C + (x[0, 2] * c * (1 / (1 + np.exp(d - a * x[:, 0]))) + b)
        A, B, C, a, b, c, d = optimize.curve_fit(f_1, x, y,
                                                 bounds=[(-2, -2, -2, 0, 0, -6, 0), (2, 2, 4, 3, 3, 0, 40)])[0]
        return A, B, C, a, b, c, d
    A, B, C, a, b, c, d = __calculate_rr__(data[flag, :, 0:3], data[flag, :, 3])
    print(A, B, C, a, b, c, d)
    Y = A * data[flag, :, 1] + B * data[flag, :, 2] + C + data[flag, 0, 2] * c * (1 / (1 + np.exp(d - a * data[flag, :, 0]))) + b
    # Y = a * data[flag, :, 1] + b * data[flag, :, 2] + c
    Y = Y.tolist()
    plt.plot(data[flag, :, 0], data[flag, 0, 2] * c * (1 / (1 + np.exp(d - a * data[flag, :, 0]))) + b)
    plt.show()
    plot_fit_v(data[flag, :, 0], data[flag, :, -1], Y)
    new = [new_y[flag, 0, 3]]  # 应该有16个值
    for i in range(1, 100):
        temp = new[-1] + Y[i]
        new.append(temp)
    plot_fitted(data[flag, :, 0], new_y[flag, :, 3], new)

get_fit_y(v_data, 0, new_y)




# plt.plot(data2[2, :, 0], data2[2, :, 3])
# plt.plot(data2[2, :, 0], new)
# plt.plot(v_data[1, :, 0], v_data[1, :, 3], label="Raw P")
# plt.plot(v_data[1, :, 0], Y, label="Fitted P")
# plt.legend()
# plt.show()