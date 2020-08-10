import numpy as np
import matplotlib.pyplot as plt
import time

class Simulated_Annealing:
    def __init__(self, dist, city_nums, alpha, T, Tmin, iters):
        self.alpha = alpha  # 退火快慢
        self.T = T  # 当前温度
        self.Tmin = Tmin  # 最低温度
        self.iters = iters  # 置换轮数
        self.length = city_nums  # 序列长度
        self.DistMat = dist

        # 新产生的序列、当前序列、最优序列
        self.sequence_new = np.arange(self.length)
        self.sequence_current = self.sequence_new.copy()
        self.sequence_best = self.sequence_new.copy()
        # 新产生的总距离、当前距离、最优距离
        self.distance_new = 0
        self.distance_current = np.inf
        self.distance_best = np.inf

    def run(self, plotStatue=False):
        start_time = time.time()
        distence_logs = []  # 距离logs
        it = 0
        while self.T > self.Tmin:  # 退火循环条件
            for i in range(self.iters):  # 类似于变异的次数，一次变异变化不大
                self.__generate_new_sequence()  # 产生新序列
                self.distance_new = self.__calc_distance(self.sequence_new)  # 计算按新序列 旅行 得到的距离
                if self.distance_new < self.distance_current:  # 距离变小 接受 并拷贝相关
                    self.distance_current = self.distance_new
                    self.sequence_current = self.sequence_new.copy()

                    if self.distance_new < self.distance_best:
                        self.distance_best = self.distance_new
                        self.sequence_best = self.sequence_new.copy()
                else:  # 距离不变下，按照一定概率接受， 概率决定由 退火 计算， 同样拷贝相关
                    if np.random.rand() < np.exp(-(self.distance_new - self.distance_current) / self.T):
                        self.distance_current = self.distance_new
                        self.sequence_current = self.sequence_new.copy()
                    else:  # 一定概率不接受
                        self.sequence_new = self.sequence_current.copy()
            self.T = self.alpha * self.T  # 降温
            distence_logs.append(self.distance_current)  # 更新日志
            print("Iters:%d" % it, "Current Distance", self.distance_current, "Best Distance", self.distance_current)
            it += 1
        over_time = time.time()
        path = self.sequence_best.tolist()
        path.append(0)
        info = ["Simulated_Annealing", str(it) + " times", str(self.distance_best) + " Km"]
        return path, info, over_time-start_time, distence_logs

    def __generate_new_sequence(self):
        '''下面的两交换和三角换是两种扰动方式，用于产生新解'''

        if np.random.rand() > 0.5:  # 交换路径中的这2个节点的顺序
            # np.random.rand()产生[0, 1)区间的均匀随机数
            while True:  # 产生两个不同的随机数
                [loc1, loc2] = np.random.randint(0, self.length - 1, 2)
                if (loc1 != loc2) & (loc1 > 0) & (loc2 > 0):
                    break
            self.sequence_new[loc1], self.sequence_new[loc2] = self.sequence_new[loc2], self.sequence_new[loc1]
        else:  # 三交换
            while True:
                [loc1, loc2, loc3] = np.random.randint(0, self.length - 1, 3)
                if ((loc1 != loc2) & (loc2 != loc3) & (loc1 != loc3) & (loc1 > 0) & (loc2 > 0) & (loc3 > 0)):
                    break

            # 下面的三个判断语句使得loc1<loc2<loc3
            if loc1 > loc2:
                loc1, loc2 = loc2, loc1
            if loc2 > loc3:
                loc2, loc3 = loc3, loc2
            if loc1 > loc2:
                loc1, loc2 = loc2, loc1

            # 下面的三行代码将[loc1,loc2)区间的数据插入到loc3之后
            tmplist = self.sequence_new[loc1:loc2].copy()
            self.sequence_new[loc1:loc3 - loc2 + 1 + loc1] = self.sequence_new[loc2:loc3 + 1].copy()
            self.sequence_new[loc3 - loc2 + 1 + loc1:loc3 + 1] = tmplist.copy()

    def __calc_distance(self, sequence):
        ''' 计算当前序列的距离 '''
        distance = 0
        for i in range(sequence.shape[0] - 1):
            distance += self.DistMat[sequence[i]][sequence[i + 1]]
        distance += self.DistMat[0][sequence[-1]]
        # print(distance)
        return distance


if __name__ == "__main__":
    coordinates = np.array([[565.0, 575.0], [25.0, 185.0], [345.0, 750.0], [945.0, 685.0], [845.0, 655.0],
                            [880.0, 660.0], [25.0, 230.0], [525.0, 1000.0], [580.0, 1175.0], [650.0, 1130.0],
                            [1605.0, 620.0], [1220.0, 580.0], [1465.0, 200.0], [1530.0, 5.0], [845.0, 680.0],
                            [725.0, 370.0], [145.0, 665.0], [415.0, 635.0], [510.0, 875.0], [560.0, 365.0],
                            [300.0, 465.0], [520.0, 585.0], [480.0, 415.0], [835.0, 625.0], [975.0, 580.0],
                            [1215.0, 245.0], [1320.0, 315.0], [1250.0, 400.0], [660.0, 180.0], [410.0, 250.0],
                            [420.0, 555.0], [575.0, 665.0], [1150.0, 1160.0], [700.0, 580.0], [685.0, 595.0],
                            [685.0, 610.0], [770.0, 610.0], [795.0, 645.0], [720.0, 635.0], [760.0, 650.0],
                            [475.0, 960.0], [95.0, 260.0], [875.0, 920.0], [700.0, 500.0], [555.0, 815.0],
                            [830.0, 485.0], [1170.0, 65.0], [830.0, 610.0], [605.0, 625.0], [595.0, 360.0],
                            [1340.0, 725.0], [1740.0, 245.0]])
    # interactive mode on
    sa = Simulated_Annealing(alpha=0.99, T=100, Tmin=1, iters=1, coordinates=coordinates)
    distence, sequence = sa.run(plotStatue=True)






