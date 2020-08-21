import random
import sys
import numpy as np
# ----------- 蚂蚁 -----------
class Ant(object):

    # 初始化
    def __init__(self, ID, V_num, H_num, car_num, HAVE, NEED, ALPHA, BETA,
                 distance, pheromone_graph, pheromone_weight_graph, q=5):

        self.ID = ID  # ID
        self.V_num = V_num
        self.H_num = H_num
        self.car_num = car_num  # 车的数量
        self.ALPHA = ALPHA
        self.BETA = BETA
        self.pheromone_graph = pheromone_graph  # 信息素矩阵 对于距离的信息素
        self.pheromone_weight_graph = pheromone_weight_graph  # 信息素矩阵 对于运载量的信息素
        self.distance = distance  # 距离矩阵
        self.__clean_data()  # 初始化出生点
        self.HAVE = HAVE  # 各疾控中心的所有
        self.NEED = NEED  # 各医院的需求
        self.q = q  # 车辆的运载量

    # 初始数据
    def __clean_data(self):

        self.path = [[random.randint(0, self.V_num - 1)]for _ in range(self.car_num)]  # 当前蚂蚁的路径
        self.weight_map = self.path.copy()  # 存储运输量的轨迹
        self.total_distance = np.zeros((self.car_num, 1), dtype=np.float)  # 当前路径的总距离
        self.total_consumption = np.zeros((self.car_num, 1), dtype=np.float)  # 当前路径的总消耗
        self.move_count = 0  # 移动次数
        self.current_city = [self.path[i][0] for i in range(self.car_num)]  # 当前停留的城市
        self.current_id = -1
        self.current_weight = [[0] for i in range(self.car_num)]  # 当前车上的重量
        self.open_table_city = [True for _ in range(self.V_num + self.H_num)]  # 探索城市的状态


        self.move_count = 1
        self.have_transfor_V = [0 for _ in range(self.V_num)]
        self.have_transfor_H = [0 for _ in range(self.H_num)]

    # 选择下一个H
    def __choice_city_at_V(self):

        next_city = -1
        select_citys_prob = np.zeros([self.H_num, 1], dtype=np.float)  # 存储去下个城市的概率
        total_prob = 0.0  # 总概率

        # 获取去下一个城市的概率
        for i in range(self.H_num):
            if self.open_table_city[self.V_num + i] and self.current_city[self.current_id] != i:
                # 计算概率：与信息素浓度成正比，与距离成反比
                select_citys_prob[i] = pow(self.pheromone_graph[self.current_city[self.current_id]][i], self.ALPHA) * pow(
                    (1.0 / self.distance[self.current_city[self.current_id]][self.V_num + i]), self.BETA)
                total_prob += select_citys_prob[i]

        # 轮盘选择城市
        if total_prob > 0.0:
            # 产生一个随机概率,0.0-total_prob
            temp_prob = random.uniform(0.0, total_prob)
            for i in range(self.H_num):
                if self.open_table_city[i]:
                    # 轮次相减
                    temp_prob -= select_citys_prob[i]
                    if temp_prob < 0.0:
                        next_city = i
                        break

        if (next_city == -1):
            next_city = random.randint(0, self.H_num - 1)
            while (self.open_table_city[self.V_num + next_city] == False):  # if==False,说明已经遍历过了
                next_city = random.randint(0, self.H_num - 1)
                # print("at_V", self.V_num + next_city)
                # print(self.open_table_city)
                # print(self.have_transfor_V)
                # print(self.HAVE)
        # 返回下一个城市序号
        # print("at_V", self.V_num + next_city)
        return self.V_num + next_city

    # 选择下一个H
    def __choice_city_at_H(self):
        '''选择V是货车在V,h的时候都能选择， 在H的时候选择H一定是车上有货'''
        next_city = -1
        select_citys_prob = np.zeros([self.V_num + self.H_num, 1], dtype=np.float)  # 存储去下个城市的概率
        total_prob = 0.0  # 总概率

        # 获取去下一个城市的概率
        for i in range(self.V_num + self.H_num):
            if self.open_table_city[i] and self.current_city[self.current_id] != i:
                # 计算概率：与信息素浓度成正比，与距离成反比
                select_citys_prob[i] = pow(self.pheromone_graph[self.current_city[self.current_id]][i], self.ALPHA) * pow(
                    (1.0 / self.distance[self.current_city[self.current_id]][i]), self.BETA)
                total_prob += select_citys_prob[i]


        # 轮盘选择城市
        if total_prob > 0.0:
            # 产生一个随机概率,0.0-total_prob
            temp_prob = random.uniform(0.0, total_prob)
            for i in range(self.V_num + self.H_num):
                if self.open_table_city[i]:
                    # 轮次相减
                    temp_prob -= select_citys_prob[i]
                    if temp_prob < 0.0:
                        next_city = i
                        break

        if (next_city == -1):
            next_city = random.randint(0, self.V_num + self.H_num - 1)
            while (self.open_table_city[next_city] == False):  # if==False,说明已经遍历过了
                next_city = random.randint(0, self.V_num + self.H_num - 1)
                print("at_H", next_city)
                print(self.open_table_city)
                print(self.have_transfor_V)
                print(self.HAVE)
        # 返回下一个城市序号

        return next_city

    # 选择下一个H
    def __choice_V_city(self):
        '''当强制让车回去时。需要选择一个V-疾控中心'''
        next_city = -1
        select_citys_prob = np.zeros([self.V_num, 1], dtype=np.float)  # 存储去下个城市的概率
        total_prob = 0.0  # 总概率

        # 获取去下一个城市的概率
        for i in range(self.V_num):
            if self.open_table_city[i] and self.current_city[self.current_id] != i:
                # 计算概率：与信息素浓度成正比，与距离成反比
                select_citys_prob[i] = pow(self.pheromone_graph[self.current_city[self.current_id]][i], self.ALPHA) * pow(
                    (1.0 / self.distance[self.current_city[self.current_id]][i]), self.BETA)
                total_prob += select_citys_prob[i]
        # 轮盘选择城市
        if total_prob > 0.0:
            # 产生一个随机概率,0.0-total_prob
            temp_prob = random.uniform(0.0, total_prob)
            for i in range(self.V_num):
                if self.open_table_city[i]:
                    # 轮次相减
                    temp_prob -= select_citys_prob[i]
                    if temp_prob < 0.0:
                        next_city = i
                        break

        if (next_city == -1):
            next_city = random.randint(0, self.V_num - 1)
            while (self.open_table_city[next_city] == False):  # if==False,说明已经遍历过了
                next_city = random.randint(0, self.V_num - 1)
                print("serch_V", next_city)
                print(self.open_table_city)
                print(self.have_transfor_V)
                print(self.HAVE)
        # 返回下一个城市序号

        return next_city

    # 选择载重量，已知下一步要走的路
    def __choice_weight(self, V_ID, next_city, have_transfor_weight, next_city_still_need):
        weight = -1
        # 下个城市还需要多少货，已经车还能装多少货，要求一个最小值
        min_weight = int(np.min([self.q - have_transfor_weight, next_city_still_need])) - 1
        if next_city_still_need >= self.q - have_transfor_weight:
            return self.q - have_transfor_weight
        # print([5 - have_transfor_weight, next_city_still_need])
        if min_weight == 0:
            return 1
        elif min_weight < 0:
            return 0

        select_weight_prob = np.zeros([min_weight, 1], dtype=np.float)  # 存储去下个城市的概率
        total_prob = 0.0  # 总概率


        for i in range(min_weight):
            # 计算概率：与信息素浓度成正比，与距离成反比
            select_weight_prob[i] = pow(self.pheromone_weight_graph[self.current_city[self.current_id]][next_city][i], self.ALPHA) \
                                     * pow((self.distance[self.current_city[self.current_id]][next_city]), self.BETA)
            total_prob += select_weight_prob[i]

        # 轮盘选择载重量
        if total_prob > 0.0:
            # 产生一个随机概率,0.0-total_prob
            temp_prob = random.uniform(0.0, total_prob)
            for i in range(min_weight):
                # 轮次相减
                temp_prob -= select_weight_prob[i]
                if temp_prob < 0.0:
                    weight = i
                    break
        # 没有选择城市则选信息素最大的
        if weight == -1:
            temp = self.pheromone_weight_graph[self.current_weight][next_city]
            for i in range(len(temp)):
                if temp[i] == np.max(temp):
                    weight = i
        # 为了判断是否把货送完
        if weight + 1 > self.HAVE[V_ID] - self.have_transfor_V[V_ID]:
            weight = self.HAVE[V_ID] - self.have_transfor_V[V_ID] - 1  # -1是为了和后面的抵消掉
            print("weight", weight)
        # print("choice weight", weight + 1)
        return weight + 1



    # 计算路径总距离
    def __cal_total_distance(self, car_ID):

        temp_distance = 0.0
        for i in range(len(self.path[car_ID]) - 1):
            start, end = self.path[car_ID][i], self.path[car_ID][i + 1]
            temp_distance += self.distance[start][end]

    # 计算总成本
    def __cal_total_consumption(self, car_ID):
        temp = 0.
        for i in range(len(self.path[car_ID]) - 1):
            start, end = self.path[car_ID][i], self.path[car_ID][i + 1]
            temp += self.distance[start][end] * (20 + self.weight_map[car_ID][i + 1])


    # 移动操作
    def __move(self, car_ID, next_city):

        self.path[car_ID].append(next_city)
        # self.open_table_city[next_city] = False
        self.total_distance[car_ID] += self.distance[self.current_city[self.current_id]][next_city]
        self.current_city[car_ID] = next_city
        self.move_count += 1

    # 过滤一些点
    def __filter_points(self):
        # 在走完全程的情况下进行过滤，减少一些无效距离
        flag = -1
        while flag == -1:
            for i in range(2, len(self.path) - 1):
                if self.path[i - 2] == self.path[i] \
                        and self.weight_map[i - 3] + self.weight_map[i - 2] + self.weight_map[i] + self.weight_map[i + 1] <= self.q \
                        and self.path[i - 2] + self.path[i] > 0:
                    del self.path[i-1:i+1]
                    self.weight_map[i - 2] += self.weight_map[i]
                    del self.weight_map[i-1:i+1]
                    break
                if i == len(self.path) - 2:
                    flag = 1

    def find_last_V(self, path):
        new = []
        for i in range(len(path)):
            if path[i] < self.V_num:
                new.append(path[i])
        return new[-1]



    # 搜索路径
    def search_path(self):

        # 初始化数据
        self.__clean_data()

        # # 先把所有的地方都送5吨的整数倍
        # for i in range(1, self.city_num):
        #     while self.need[i] - self.have_transfor[i] >= self.q:
        #         self.__move(i)
        #         self.weight_map.append(self.q)
        #         self.__move(0)
        #         self.weight_map.append(0)
        #         self.have_transfor[i] += self.q
        #         self.have_transfor[0] -= self.q
        fff = 0
        while self.have_transfor_V != self.HAVE:
            # 每个车辆开始走，与单车辆多次数走的不同在于，多车辆初始点不同
            # 多个取货点变化更多
            for id in range(self.car_num):
                self.current_id = id
                # 货物为0时直接回城市0
                self.current_weight = -1
                have_transfor_weight = 0
                move_times = 0
                # 当前的货送不完不回去

                while have_transfor_weight != 5:
                    print(self.have_transfor_V)
                    # 记录已经装了多少
                    # 只根据距离选择下个点
                    next_city = -1
                    if self.current_city[self.current_id] < self.V_num:  # 说明此时在疾控中心
                        next_city = self.__choice_city_at_V()
                    else:
                        next_city = self.__choice_city_at_H()
                    if next_city < self.V_num and self.path[id][-1] > self.V_num:  # 说明下一趟走疾控中心
                        self.__move(id, next_city)

                        self.weight_map[id].append(0)  # 此时无须更新运送量
                        break  # 跳出循环，让下一辆车开始走
                    # 计算下个点需要的物资
                    next_city_still_need = self.NEED[next_city - self.V_num] - self.have_transfor_H[next_city - self.V_num]
                    # 如果下个点需要的物资够了，加到禁忌表，再进行新一轮选点，否则，就走过去
                    if next_city_still_need == 0:
                        self.open_table_city[next_city] = False
                        continue
                    if self.current_city[self.current_id] < self.V_num and next_city < self.V_num:
                        print("不能V->V")
                        continue
                    V_ID = self.find_last_V(self.path[id])
                    print(V_ID)
                    if self.have_transfor_V[V_ID] == self.HAVE[V_ID]:
                        self.open_table_city[V_ID] = False
                        V_City = self.__choice_V_city()
                        self.__move(id, V_City)  # 最后的一个路径必须回到0
                        self.weight_map.append(0)
                        break

                    self.current_weight = self.__choice_weight(V_ID, next_city, have_transfor_weight, next_city_still_need)
                    if self.current_weight == 0:
                        break
                    self.__move(id, next_city)
                    move_times += 1


                    print("weight", self.current_weight)
                    # 如果下个城市需要的物资比车子装的多，current_weight = 0，否则就减去下个城市需要的量
                    if next_city_still_need >= self.current_weight:
                        self.have_transfor_V[V_ID] += self.current_weight
                        self.have_transfor_H[next_city-self.V_num] += self.current_weight  # 收到的货要更新
                        self.weight_map[id].append(int(self.current_weight))  # 路径送货量要记录
                        have_transfor_weight += self.current_weight
                        self.current_weight = 0  # 车上装了多少要更新
                    elif next_city_still_need < self.current_weight:
                        self.have_transfor_V[V_ID] += next_city_still_need
                        self.have_transfor_H[next_city-self.V_num] += next_city_still_need   # 收到的货要更新
                        self.weight_map[id].append(int(next_city_still_need))  # 路径送货量要记录
                        self.current_weight -= next_city_still_need    # 车上装了多少要更新
                        have_transfor_weight += next_city_still_need

                    for i in range(self.V_num):
                        if self.HAVE[i] == self.have_transfor_V[i]:
                            self.open_table_city[i] = False

                    if have_transfor_weight == 5 or move_times >= 2:
                        V_City = self.__choice_V_city()
                        self.__move(id, V_City)  # 最后的一个路径必须回到0
                        self.weight_map.append(0)
                        break
            # print(self.weight_map)
            # self.__filter_points()
            # print(self.weight_map)
        # 计算路径总长度
        for i in range(self.car_num):
            self.total_consumption = self.__cal_total_consumption(i)
            self.total_distance = self.__cal_total_distance(i)