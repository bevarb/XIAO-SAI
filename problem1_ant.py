
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

    """===============================算法参数设置==============================="""
    # 参数
    '''
    ALPHA:信息启发因子，值越大，则蚂蚁选择之前走过的路径可能性就越大
          ，值越小，则蚁群搜索范围就会减少，容易陷入局部最优
    BETA:Beta值越大，蚁群越就容易选择局部较短路径，这时算法收敛速度会
         加快，但是随机性不高，容易得到局部的相对最优
    '''
    ALPHA, BETA, RHO, Q = 1.0, 2.0, 0.5, 100.0
    # 城市数，蚁群
    city_num, ant_num = 30, 60

    # 城市距离和信息素
    distance_graph = dist
    pheromone_graph = [[1.0 for col in range(city_num)] for raw in range(city_num)]
    """==================================搜索==================================="""
    ants = [Ant(ID, city_num, ALPHA, BETA, distance_graph, pheromone_graph) for ID in range(ant_num)]  # 初始蚁群
    best_ant = Ant(-1, city_num, ALPHA, BETA, distance_graph, pheromone_graph)  # 初始最优解
    best_ant.total_distance = 1 << 31  # 初始最大距离
    iter = 1  # 初始化迭代次数
    Total_iter = 50
    # 开始搜索
    for i in range(Total_iter):

        # 遍历每一只蚂蚁
        for ant in ants:
            # 搜索一条路径

            ant.search_path()
            # 与当前最优蚂蚁比较
            if ant.total_distance < best_ant.total_distance:
                # 更新最优解
                best_ant = copy.deepcopy(ant)
        # 更新信息素
        # 获取每只蚂蚁在其路径上留下的信息素
        temp_pheromone = [[0.0 for col in range(city_num)] for raw in range(city_num)]
        for ant in ants:
            for i in range(1, city_num):
                start, end = ant.path[i - 1], ant.path[i]
                # 在路径上的每两个相邻城市间留下信息素，与路径总距离反比
                temp_pheromone[start][end] += Q / ant.total_distance
                temp_pheromone[end][start] = temp_pheromone[start][end]

        # 更新所有城市之间的信息素，旧信息素衰减加上新迭代信息素
        for i in range(city_num):
            for j in range(city_num):
                pheromone_graph[i][j] = pheromone_graph[i][j] * RHO + temp_pheromone[i][j]
        print(u"迭代次数：", iter, u"最佳路径总距离：", int(best_ant.total_distance))
        iter += 1
    print(best_ant.path)
    info = ["Ants Method", str(Total_iter) + " times", str(int(best_ant.total_distance)) + " Km"]
    vi.arrow_map(base_map, best_ant.path, info)














