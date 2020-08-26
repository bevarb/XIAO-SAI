import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Model_3.plot.plot_RS import plot_RS, plot_v, plot_fit_v, plot_fitted, plot_diff_sig
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

# 获得插值数据
new_x = np.arange(0, 100, 1)
new_y = np.zeros([6, 100, 4], dtype=np.float)
for i in range(3):
    if i !=3:
        iy3_cod = get_spi(new_x, data2[i, :, 0], data2[i, :, 1], 3)
        iy3_rs = get_spi(new_x, data2[i, :, 0], data2[i, :, 2], 3)
        iy3_p = get_spi(new_x, data2[i, :, 0], data2[i, :, 3], 3)
        new_y[i, :, 0] = new_x
        new_y[i, :, 1] = iy3_cod
        new_y[i, :, 2] = iy3_rs
        new_y[i, :, 3] = iy3_p



def get_fit_y(new_y):
    X = np.zeros([3, 100, 2], dtype=np.float)
    for i in range(3):
        X[i, :, 0] = new_y[0, :, 0]
        X[i, :, 1] = new_y[i, 0, 2]

    def __calculate_rr__(X, Y):
        x = X.reshape([300, 2])
        y = Y.reshape([300, 1]).ravel()
        def f_1(x, a, b, c, d):
            result = c * (1 / (1 + np.exp(d * x[:, 0] - a * x[:, 1]))) + b
            # result = result.ravel()
            return result

        a, b, c, d = optimize.curve_fit(f_1, x, y,
                                        bounds=([0.1, 0, 20, 1.1], [0.16, 10, 60, 1.2]))[0]

        y_pred = c * (1 / (1 + np.exp(d * x[:, 0] - a * x[:, 1]))) + b
        y_mean = np.mean(y)
        r2 = 1 - np.sum(np.square((y_pred - y))) / np.sum(np.square(y_mean - y))
        return a, b, c, d, r2

    a, b, c, d, r2 = __calculate_rr__(X, new_y[0:3, :, 2])
    print("a:%.3f,b:%.3f,c:%.3f,d:%.3f," % (a, b, c, d), r2)

    for i in range(1):
        Yi = c * (1 / (1 + np.exp(d * X[i, :, 0] - a * X[i, :, 1]))) + b - 5
        new_y[3 + i, :, 2] = Yi

    plot_RS(new_y)

# def analyze_fit_y(data, flag, new_y):
#     def __calculate_rr__(x, y):
#         def f_1(x, A, B, C, a, b, c, d):
#             return A * x[:, 1] + B * x[:, 2] + C + (x[0, 2] * c * (1 / (1 + np.exp(d - a * x[:, 0]))) + b)
#         A, B, C, a, b, c, d = optimize.curve_fit(f_1, x, y,
#                                                  bounds=[(-2, -2, -2, 0, -4, -2, 40), (2, 2, 4, 5, 6, -1, 60)])[0]
#         return A, B, C, a, b, c, d
#     A, B, C, a, b, c, d = __calculate_rr__(data[flag, :, 0:3], data[flag, :, 3])
#     print( A, B, C, a, b, c, d)
#     datas = []
#     labels = []
#     for i in range(0, 5):
#         step = i / 20
#         Y = A * data[flag, :, 1] + B * data[flag, :, 2] + C + (data[flag, 0, 2] + step) * c * (1 / (1 + np.exp(d - a * data[flag, :, 0]))) + b
#         Y = Y.tolist()
#         new = [new_y[flag, 0, 3]]
#         for i in range(1, 100):
#             temp = new[-1] + Y[i]
#             new.append(temp)
#         datas.append(new)
#         labels.append(step)
#     plot_diff_sig(datas, labels)


get_fit_y(new_y)  # 拟合
# analyze_fit_y(v_data, 1, new_y)  # 分析参数



