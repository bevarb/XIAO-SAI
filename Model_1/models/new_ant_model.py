import random
import sys
import numpy as np
# ----------- 蚂蚁 -----------
class Ant(object):

    # 初始化
    def __init__(self, ID, city_num, car_nums, ALPHA, BETA, distance_graph, pheromone_graph, v=4, r=4, c=4,):

        self.ID = ID  # ID
        self.city_num = city_num  # 城市数量
        self.car_num = car_nums  # 车的数量
        self.v = v  # 车行驶的速度
        self.r = r  # 充电速率
        self.c = c  # 耗电速率
        self.ALPHA = ALPHA
        self.BETA = BETA
        self.pheromone_graph = pheromone_graph
        # 增加三维矩阵
        self.distance_graph = np.zeros((city_num + car_nums - 1, city_num + car_nums - 1), dtype=np.float)
        self.distance_graph[:city_num, :city_num] = distance_graph
        for i in range(car_nums - 1):
            self.distance_graph[city_num + i, :] = self.distance_graph[0, :]
            self.distance_graph[:, city_num + i] = self.distance_graph[:, 0]
        self.__clean_data()  # 随机初始化出生点

    # 初始数据
    def __clean_data(self):

        self.path = [0]  # 当前蚂蚁的路径
        self.total_distance = 0.0  # 当前路径的总距离
        self.move_count = 0  # 移动次数
        self.current_city = 0  # 当前停留的城市
        self.open_table_city = [True for _ in range(self.city_num + self.car_num - 1)]  # 探索城市的状态
        '''起点必须是0，所以不用随机初始化'''
        # city_index = random.randint(0, self.city_num - 1)  # 随机初始出生点, 随机一个
        # self.current_city = city_index
        # self.path.append(city_index)
        self.open_table_city[self.current_city] = False
        self.move_count = 1

    # def __get_time_graph(self):
    #     self.time_graph = np.zeros((30, 30), dtype=np.float)
    #     for i in range(self.city_num - 1):
    #         run_time = self.distance_graph[i, i+1] / self.v
    #         cong_time = self.c[i + 1]

    # 选择下一个城市
    def __choice_next_city(self):

        next_city = -1
        select_citys_prob = [0.0 for _ in range(self.city_num + self.car_num - 1)]  # 存储去下个城市的概率
        total_prob = 0.0

        # 获取去下一个城市的概率
        for i in range(self.city_num + self.car_num - 1):
            if self.open_table_city[i]:
                # 计算概率：与信息素浓度成正比，与距离成反比(修改为与时间成反比)
                if (self.current_city > self.city_num - 1 and i > self.city_num - 1) or (self.current_city == 0 and i > self.city_num - 1):
                    select_citys_prob[i] = - 100
                else:
                    select_citys_prob[i] = pow(self.pheromone_graph[self.current_city][i], self.ALPHA) * pow(
                        (1.0 / self.distance_graph[self.current_city][i]), self.BETA)
                    total_prob += select_citys_prob[i]

        # 轮盘选择城市
        if total_prob > 0.0:
            # 产生一个随机概率,0.0-total_prob
            temp_prob = random.uniform(0.0, total_prob)
            for i in range(self.city_num + self.car_num - 1):
                if self.open_table_city[i]:
                    # 轮次相减
                    temp_prob -= select_citys_prob[i]
                    if temp_prob < 0.0:
                        next_city = i
                        break
        while (self.current_city > self.city_num - 1 and next_city > self.city_num - 1) or (self.current_city == 0 and next_city > self.city_num - 1):
            for i in range(self.city_num + self.car_num - 1):
                if self.open_table_city[i]:
                    next_city = i
                    break

        if (next_city == -1):
            next_city = random.randint(0, self.city_num + self.car_num - 2)  # 随机数右边的边界也能够生成，所以-2
            while ((self.open_table_city[next_city]) == False):  # if==False,说明已经遍历过了
                next_city = random.randint(0, self.city_num + self.car_num - 2)  # 随机数右边的边界也能够生成，所以-2

        # 返回下一个城市序号
        return next_city

    # 计算路径总距离
    def __cal_total_distance(self):

        temp_distance = 0.0
        for i in range(len(self.path) - 1):
            start, end = self.path[i], self.path[i + 1]
            temp_distance += self.distance_graph[start][end]
        self.total_distance = temp_distance

    # 移动操作
    def __move(self, next_city):

        self.path.append(next_city)
        self.open_table_city[next_city] = False
        self.total_distance += self.distance_graph[self.current_city][next_city]
        self.current_city = next_city
        self.move_count += 1

    # 搜索路径
    def search_path(self):

        # 初始化数据
        self.__clean_data()

        # 搜素路径，遍历完所有城市为止
        while self.move_count < self.city_num + self.car_num - 1:
            # 移动到下一个城市
            next_city = self.__choice_next_city()
            self.__move(next_city)
        self.__move(0)  # 最后的一个路径必须回到0
        # 计算路径总长度
        self.__cal_total_distance()