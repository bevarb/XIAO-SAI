import random
import sys
# ----------- 蚂蚁 -----------
class Ant(object):

    # 初始化
    def __init__(self, ID, car_nums, v, r, c, city_num, ALPHA, BETA, distance_graph, pheromone_graph):

        self.ID = ID  # ID
        self.city_num = city_num  # 城市数量
        self.car_num = car_nums  # 车的数量
        self.v = v  # 车行驶的速度
        self.r = r  # 充电速率
        self.c = c  # 耗电速率
        self.ALPHA = ALPHA
        self.BETA = BETA
        self.pheromone_graph = pheromone_graph
        self.distance_graph = distance_graph
        self.__clean_data()  # 随机初始化出生点

    # 初始数据
    def __clean_data(self):

        self.path = [0]  # 当前蚂蚁的路径
        self.total_distance = 0.0  # 当前路径的总距离
        self.move_count = 0  # 移动次数
        self.current_city = 0  # 当前停留的城市
        self.open_table_city = [True for _ in range(self.city_num)]  # 探索城市的状态
        '''起点必须是0，所以不用随机初始化'''
        # city_index = random.randint(0, self.city_num - 1)  # 随机初始出生点, 随机一个
        # self.current_city = city_index
        # self.path.append(city_index)
        self.open_table_city[self.current_city] = False
        self.move_count = 1

    def __get_time_graph(self):

    # 选择下一个城市
    def __choice_next_city(self):

        next_city = -1
        select_citys_prob = [0.0 for _ in range(self.city_num)]  # 存储去下个城市的概率
        total_prob = 0.0

        # 获取去下一个城市的概率
        for i in range(self.city_num):
            if self.open_table_city[i]:
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
            while ((self.open_table_city[next_city]) == False):  # if==False,说明已经遍历过了
                next_city = random.randint(0, self.city_num - 1)

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
        while self.move_count < self.city_num:
            # 移动到下一个城市
            next_city = self.__choice_next_city()
            self.__move(next_city)
        self.__move(0)  # 最后的一个路径必须回到0
        # 计算路径总长度
        self.__cal_total_distance()