
import copy

from models.ant_model import Ant

import pandas as pd
import numpy as np
from libs.visulize import visulize
from libs.tools import millerToXY, get_dist

if __name__ == "__main__":
    data = pd.read_excel("data.xlsx")
    lonlat = data.loc[0:30]
    real_data = []
    for i in range(len(lonlat)):
        x, y = millerToXY(lonlat.loc[i]["传感器经度"], lonlat.loc[i]["传感器纬度"])
        real_data.append([x, y, i])
    real_data = np.array(real_data)
    x_min, y_min = np.min(real_data[:, 0]), np.min(real_data[:, 1])
    x_max, y_max = np.max(real_data[:, 0]), np.max(real_data[:, 1])
    real_data = real_data - np.array([x_min, y_min, 0])
    # 可视化基本地图
    vi = visulize()
    base_map = vi.base_map(real_data)
    # 求解距离矩阵
    dist = np.zeros((30, 30), np.uint8)
    for i in range(len(real_data)):
        for j in range(len(real_data)):
            dist[i][j] = get_dist(real_data[i], real_data[j])
    path = [0, 2, 1, 9, 8, 12, 15, 27, 16, 13, 10, 5, 3, 4, 21, 23, 22,
            28, 25, 24, 14, 11, 6, 7, 18, 26, 29, 19, 20, 17, 0]
    Total = 0
    for i in range(len(dist) - 1):
        Total += dist[path[i], path[i+1]]
    print(Total)