import random
import sys
import numpy as np
# ----------- 蚂蚁 -----------
class Ant(object):

    # 初始化
    def __init__(self, ID, city_num, need, ALPHA, BETA,
                 distance_graph, pheromone_graph, pheromone_weight_graph, q=5):

        self.ID = ID  # ID
        self.city_num = city_num  # 城市数量
        self.ALPHA = ALPHA
        self.BETA = BETA
        self.pheromone_graph = pheromone_graph  # 信息素矩阵 对于距离的信息素
        self.pheromone_weight_graph = pheromone_weight_graph  # 信息素矩阵 对于运载量的信息素
        self.distance_graph = distance_graph  # 距离矩阵
        self.__clean_data()  # 初始化出生点
        self.need = need  # 各地方的需求量
        self.q = q  # 车辆的运载量

    # 初始数据
    def __clean_data(self):

        self.path = [0]  # 当前蚂蚁的路径
        self.weight_map = [0]  # 存储运输量的轨迹
        self.total_distance = 0.0  # 当前路径的总距离
        self.total_consumption = 0.0  # 当前路径的总消耗
        self.move_count = 0  # 移动次数
        self.current_city = 0  # 当前停留的城市
        self.current_weight = 0  # 当前车上的重量
        self.open_table_city = [True for _ in range(self.city_num)]  # 探索城市的状态
        # self.open_table_city[0] = False  # 供货点不能主动过去，只能等货送完强制回去补货
        '''起点必须是0，所以不用随机初始化'''
        self.move_count = 1
        self.have_transfor = [0 for _ in range(self.city_num)]

    # 选择下一个城市
    def __choice_next_city(self):

        next_city = -1
        select_citys_prob = np.zeros([self.city_num, 1], dtype=np.float)  # 存储去下个城市的概率
        total_prob = 0.0  # 总概率

        # 获取去下一个城市的概率
        for i in range(self.city_num):
            if self.open_table_city[i] and self.current_city != i:
                try:
                    # 计算概率：与信息素浓度成正比，与距离成反比
                    select_citys_prob[i] = pow(self.pheromone_graph[self.current_city][i], self.ALPHA) * pow(
                        (1.0 / self.distance_graph[self.current_city][i]), self.BETA)
                    total_prob += select_citys_prob[i]
                except ZeroDivisionError as e:
                    print('Ant ID: {ID}, current city: {current}, target city: {target}'.format(ID=self.ID,
                                                                                                current=self.current_city,
                                                                                                target=i))
                    sys.exit(1)

        # 轮盘选择城市
        if total_prob > 0.0:
            # 产生一个随机概率,0.0-total_prob
            temp_prob = random.uniform(0.0, total_prob)
            for i in range(self.city_num):
                if self.open_table_city[i]:
                    # 轮次相减
                    temp_prob -= select_citys_prob[i]
                    if temp_prob < 0.0:
                        next_city = i
                        break

        # 未从概率产生，顺序选择一个未访问城市
        # if next_city == -1:
        #     for i in range(city_num):
        #         if self.open_table_city[i]:
        #             next_city = i
        #             break

        if (next_city == -1):
            next_city = random.randint(0, self.city_num - 1)
            while (self.open_table_city[next_city] == False):  # if==False,说明已经遍历过了
                next_city = random.randint(0, self.city_num - 1)

        # 返回下一个城市序号
        return next_city

    # 选择载重量，已知下一步要走的路
    def __choice_weight(self, next_city, have_transfor_weight, next_city_still_need):
        weight = -1
        # # 下个城市还需要多少货，已经车还能装多少货，要求一个最小值
        min_weight = int(np.min([5 - have_transfor_weight, next_city_still_need])) - 1
        if next_city_still_need >= 5 - have_transfor_weight:
            return 5 - have_transfor_weight
        # print([5 - have_transfor_weight, next_city_still_need])
        if min_weight == 0:
            return 1
        elif min_weight < 0:
            return 0

        select_weight_prob = np.zeros([min_weight, 1], dtype=np.float)  # 存储去下个城市的概率
        total_prob = 0.0  # 总概率

        # 获取去下一个城市的概率
        for i in range(min_weight):
            # 计算概率：与信息素浓度成正比，与距离成反比
            select_weight_prob[i] = pow(self.pheromone_weight_graph[self.current_city][next_city][i], self.ALPHA) \
                                    * pow((self.distance_graph[self.current_city][next_city]), self.BETA)
            total_prob += select_weight_prob[i]


        # 轮盘选择城市
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
        if weight + 1 > 100 + self.have_transfor[0]:
            weight = 100 + self.have_transfor[0] - 1  # -1是为了和后面的抵消掉
        # print("choice weight", weight + 1)
        return weight + 1



    # 计算路径总距离
    def __cal_total_distance(self):

        temp_distance = 0.0
        for i in range(len(self.path) - 1):
            start, end = self.path[i], self.path[i + 1]
            temp_distance += self.distance_graph[start][end]
        return temp_distance

    # 计算总成本
    def __cal_total_consumption(self):
        temp = 0.
        for i in range(len(self.path) - 1):
            start, end = self.path[i], self.path[i + 1]
            temp += self.distance_graph[start][end] * (20 + self.weight_map[i + 1])
        return temp


    # 移动操作
    def __move(self, next_city):

        self.path.append(next_city)
        # self.open_table_city[next_city] = False
        self.total_distance += self.distance_graph[self.current_city][next_city]
        self.current_city = next_city
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




    # 搜索路径
    def search_path(self):

        # 初始化数据
        self.__clean_data()

        # 先把所有的地方都送5吨的整数倍
        # for i in range(1, self.city_num):
        #     while self.need[i] - self.have_transfor[i] >= self.q:
        #         self.__move(i)
        #         self.weight_map.append(self.q)
        #         self.__move(0)
        #         self.weight_map.append(0)
        #         self.have_transfor[i] += self.q
        #         self.have_transfor[0] -= self.q


        # 搜素路径，直到城市0处的物资被运送完
        while self.have_transfor[0] != self.need[0]:
            # 从城市0开始，到城市0结束，为一轮
            # 货物为0时直接回城市0
            self.current_weight = -1
            have_transfor_weight = 0
            move_times = 0
            # 当前的货送不完不回去
            while have_transfor_weight != 5:
                # 记录已经装了多少
                # 只根据距离选择下个点
                next_city = self.__choice_next_city()
                # 计算下个点需要的物资
                next_city_still_need = self.need[next_city] - self.have_transfor[next_city]
                # 如果下个点需要的物资够了，加到禁忌表，再进行新一轮选点，否则，就走过去
                if self.current_city != 0 and next_city == 0:
                    self.__move(0)  # 最后的一个路径必须回到0
                    self.weight_map.append(0)
                    break
                if next_city_still_need == 0 and next_city != 0:
                    self.open_table_city[next_city] = False
                    continue
                else:
                    self.current_weight = self.__choice_weight(next_city, have_transfor_weight, next_city_still_need)
                    if self.current_weight == 0:
                        break
                    self.__move(next_city)
                    move_times += 1

                # 如果下个城市需要的物资比车子装的多，current_weight = 0，否则就减去下个城市需要的量
                if next_city_still_need >= self.current_weight:
                    self.have_transfor[next_city] += self.current_weight  # 收到的货要更新
                    self.weight_map.append(int(self.current_weight))  # 路径送货量要记录
                    self.have_transfor[0] -= self.current_weight  # 送出的货要更新
                    have_transfor_weight += self.current_weight
                    self.current_weight = 0  # 车上装了多少要更新

                elif next_city_still_need < self.current_weight:
                    self.have_transfor[next_city] += next_city_still_need  # 收到的货要更新
                    self.weight_map.append(int(next_city_still_need))  # 路径送货量要记录
                    self.have_transfor[0] -= next_city_still_need  # 送出的货要更新
                    self.current_weight -= next_city_still_need    # 车上装了多少要更新
                    have_transfor_weight += next_city_still_need
                if have_transfor_weight == 5 or move_times >= 2:
                    self.__move(0)  # 最后的一个路径必须回到0
                    self.weight_map.append(0)
        # print(self.weight_map)
        self.__filter_points()
        # print(self.weight_map)
        # 计算路径总长度
        self.total_consumption = self.__cal_total_consumption()
        self.total_distance = self.__cal_total_distance()