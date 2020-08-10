
import pandas as pd
import numpy as np
from libs.visulize import visulize, plot_iter
from libs.tools import millerToXY, get_dist, getDistance
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 步骤一（替换sans-serif字体）
plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）
def get_B(route, dist, v, r, c,):
    def t_wait(t_wait_map, route, dist, v, r, c, i):
        total_L = 0
        # 计算路程时间
        for k in range(i):
            total_L += dist[route[k], route[k+1]]  # i=1 则距离为0->1，range默认从0开始
        run_time = total_L / v
        # 计算充电时间
        r_time = 0.0
        for k in range(1, i-1):
            r_time += (t_wait_map[k] * c[k]) / (r - c[k])
        return run_time + r_time
    def t_pass(t_wait_map, r, c, i):
        t_pass_total = t_wait_map[29] + (t_wait_map[29] * c[29])/(r - c[29])
        t_pass_time = t_pass_total - t_wait_map[i] - (t_wait_map[i]*c[i])/(r-c[i])
        return t_pass_time
    # 初始化
    t_wait_map = np.zeros((30, 1), dtype=np.float)
    t_pass_map = np.zeros((30, 1), dtype=np.float)

    for i in range(0, 30):
        t_wait_map[i] = np.round(t_wait(t_wait_map, route, dist, v, r, c, i), 3)
    for i in range(1, 29):
        t_pass_map[i] = np.round(t_pass(t_wait_map, r, c, i), 3)
    # 计算电池容量， 时间最长的×耗电速率就是电池容量
    B = np.zeros((29, 1), dtype=np.float)
    logs = []
    for i in range(1, 30):
        t = t_wait_map[i] if t_wait_map[i] > t_pass_map[i] else t_pass_map[i]
        B[i - 1] = np.round(t * c[i], 3)
        logs.append([route[i], c[i], float(t_wait_map[i]), float(t_pass_map[i]), float(B[i - 1])])
    return B, logs




if __name__ == "__main__":
    data = pd.read_excel("data.xlsx")
    lonlat = data.loc[0:30]

    # 求解距离矩阵
    dist = np.zeros((30, 30), np.float)
    for i in range(30):
        for j in range(30):
            dist[i][j] = getDistance(lonlat.loc[i]["传感器经度"], lonlat.loc[i]["传感器纬度"],
                                     lonlat.loc[j]["传感器经度"], lonlat.loc[j]["传感器纬度"])
    C = lonlat.loc[:]["能量消耗速率(mA/h)"]
    route = [0, 2, 1, 9, 7, 6, 14, 11, 8, 12, 15, 27, 16, 13, 10,
             5, 3, 4, 22, 28, 24, 23, 21, 17, 20, 18, 25, 26, 29, 19, 0]
    # B, logs = get_B(route, dist, v=30, r=30, c=C)
    # for log in logs:
    #      print(log)
    # lo = pd.DataFrame(logs)
    # lo.to_excel("logs.xlsx")
    # B_ = [[], [], []]
    # label = []
    # for r in range(20, 100, 1):
    #     B, logs = get_B(route, dist, v=30, r=r, c=C)
    #     if r == 20:
    #         label.append([logs[4][0], logs[9][0], logs[13][0]])
    #     B_[0].append(logs[4][-1])
    #     B_[1].append(logs[9][-1])
    #     B_[2].append(logs[13][-1])
    #
    # for i in range(3):
    #     plt.plot([r for r in range(20, 100, 1)], B_[i], label="Sensor %d" % label[0][i])
    # plt.xlabel("充电速率r")
    # plt.legend()
    # plt.ylabel("传感器电池容量B")
    # plt.title("充电速率r与传感器电池容量B的灵敏度曲线")
    # plt.show()
    B_ = [[], [], []]
    label = []
    for v in range(5, 100, 1):
        B, logs = get_B(route, dist, v=v, r=30, c=C)
        if v == 5:
            label.append([logs[4][0], logs[9][0], logs[13][0]])
        B_[0].append(logs[4][-1])
        B_[1].append(logs[9][-1])
        B_[2].append(logs[13][-1])

    for i in range(3):
        plt.plot([r for r in range(5, 100, 1)], B_[i], label="Sensor %d" % label[0][i])
    plt.xlabel("移动速率v")
    plt.legend()
    plt.ylabel("传感器电池容量B")
    plt.title("移动速率v与传感器电池容量B的灵敏度曲线")
    plt.show()