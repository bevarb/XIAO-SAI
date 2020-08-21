import copy
from Model_2.models.new_ant_model import Ant

import pandas as pd
import numpy as np
from Model_2.libs.visulize import visulize, plot_iter
# from Model_2.libs.tools import millerToXY, get_dist, getDistance
import time
def ants_method(distance_graph, HAVE, NEED, Total_iter,car_num=4,  V_num=11, H_num=15,
                ALPHA=1.0, BETA=2.0, RHO=0.4, Q=100.0, ant_num=30):
    """===============================算法参数设置==============================="""
    # 参数
    '''
    ALPHA:信息启发因子，值越大，则蚂蚁选择之前走过的路径可能性就越大
          ，值越小，则蚁群搜索范围就会减少，容易陷入局部最优
    BETA:Beta值越大，蚁群越就容易选择局部较短路径，这时算法收敛速度会
         加快，但是随机性不高，容易得到局部的相对最优
    '''
    start_time = time.time()
    pheromone_graph = np.ones([V_num + H_num, V_num + H_num], dtype=np.float)
    pheromone_weight_graph = np.ones([V_num + H_num, V_num + H_num, 5], dtype=np.float)
    """==================================搜索==================================="""
    ants = [Ant(ID, V_num, H_num, car_num, HAVE, NEED, ALPHA, BETA, distance_graph, pheromone_graph, pheromone_weight_graph) for ID in range(ant_num)]  # 初始蚁群
    best_ant = Ant(-1, V_num, H_num, car_num, HAVE, NEED, ALPHA, BETA, distance_graph, pheromone_graph, pheromone_weight_graph)  # 初始最优解
    best_ant.total_distance = 1 << 31  # 初始最大距离
    iter = 1  # 初始化迭代次数
    logs = []
    # 开始搜索
    for i in range(Total_iter):
        # 遍历每一只蚂蚁
        for ant in ants:
            # 搜索一条路径
            ant.search_path()
            # 与当前最优蚂蚁比较
            if np.sum(ant.total_distance) < np.sum(best_ant.total_distance):
                # 更新最优解
                best_ant = copy.deepcopy(ant)
        logs.append(best_ant.total_distance)
        # 更新信息素
        # 获取每只蚂蚁在其路径上留下的信息素
        temp_pheromone = np.zeros([V_num + H_num, V_num + H_num], dtype=np.float)
        temp_pheromone_weight = np.zeros([V_num + H_num, V_num + H_num, 5], dtype=np.float)
        for ant in ants:
            # 修改为路程，原来是城市只能走一趟，现在很多要走多趟
            for i in range(len(ant.path)):
                for j in range(1, len(ant.path[i])):
                    start, end = ant.path[j - 1], ant.path[j]
                    # 在路径上的每两个相邻城市间留下信息素，与路径总距离反比
                    total = 0.5 * ant.total_distance[i] + 0.025 * ant.total_consumption[i]
                    temp_pheromone[start][end] += Q / total
                    temp_pheromone[end][start] = temp_pheromone[start][end]
                    # 关于运输物资量的信息素
                    temp_pheromone_weight[start][end][ant.weight_map[i][ant.path[i][j]] - 1] += Q / total

        # 更新所有城市之间的信息素，旧信息素衰减加上新迭代信息素
        pheromone_graph = pheromone_graph * RHO + temp_pheromone
        pheromone_weight_graph += pheromone_weight_graph * RHO + temp_pheromone_weight
        print(u"迭代次数：", iter, u"最佳路径总距离：", round(best_ant.total_distance, 3),
              u"最佳成本损耗：", round(best_ant.total_consumption, 3))
        iter += 1
    end_time = time.time()
    info = ["Ants Method", str(Total_iter) + " times", str(round(best_ant.total_distance, 3)) + " Km"]

    return best_ant.path, best_ant.weight_map, info, end_time - start_time, logs


if __name__ == "__main__":
    data = pd.read_excel("data/Hospital_lng_lat_data.xlsx")
    lonlat = data.loc[0:]
    real_data = []
    name = []
    for i in range(len(lonlat)):
        real_data.append([lonlat.loc[i]["lng"] * 1000, lonlat.loc[i]["lat"] * 1000, i])
        name.append(lonlat.loc[i]["转换后名称"])
    real_data = np.array(real_data)
    x_min, y_min = np.min(real_data[:, 0]), np.min(real_data[:, 1])
    real_data = real_data - np.array([x_min, y_min, 0])
    # 可视化基本地图
    vi = visulize()
    base_map = vi.base_map(real_data, name)
    # 求解距离矩阵
    dist_file = pd.read_excel("data/dist_CH_noLoad.xlsx")
    dist = np.zeros((11 + 15, 11 + 15), np.float)
    for i in range(11 + 15):
        for j in range(1, 12):
            dist[i, j - 1] = float(dist_file.loc[i]["C%d" % j])
        for j in range(0, 15):
            dist[i, 11 + j] = float(dist_file.loc[i]["H%d" % j])
    HAVE = [7, 6, 7, 9, 8, 11, 10, 8, 4, 16, 14]
    NEED = [20, 15, 10, 5, 7, 6, 10, 7, 4, 3, 5, 5, 1, 1, 1]
    # 蚁群算法
    path, weight, info, pass_time, logs = ants_method(dist, HAVE, NEED, 1000, ALPHA=1.0, BETA=1.8, ant_num=80)
    #
    plot_iter(logs)
    print(path)
    print(weight)
    print(info)
    print(pass_time)
    #
    # vi.arrow_map(base_map, path, info)
















