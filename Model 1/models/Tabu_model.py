import random
import time
class tabusearch():
    # s1 = datetime.datetime.now()  # 获取运行前的时间

    def __init__(self, dist, city_nums, diedaitimes, cacu_time, tabu_length, origin_times):
        self.dist = dist
        self.diedaitimes = diedaitimes
        self.cacu_time = cacu_time
        self.tabu_length = tabu_length
        self.origin_times = origin_times
        self.city_nums = city_nums

    def pan_move(self, move_step,tabu_move):
        # 判断移动是否在禁忌区域中，如果是返回True和该点索引，否则返回False和0
        if move_step in tabu_move:
            index = tabu_move.index(move_step)
            return(True, index)
        else:
            return(False, 0)
    def pan_cost(self, cost, tabu_cost,t):
        # 判断该移动是否比禁忌区域中该移动小，如果小则返回True，否则返回False
        if cost < tabu_cost[t]:
            return True
        else:
            return False
    def add_tabu(self, cost, move, tabu_cost, tabu_move, t):
        # 为禁忌区域添加移动和成本，若超过T则剔除最先进入的禁忌
        tabu_cost.append(cost)
        tabu_move.append(move)
        if len(tabu_cost) > t:
            del tabu_cost[0]
        if len(tabu_move) > t:
            del tabu_move[0]
        return(tabu_cost,tabu_move)
    def cacu(self, vec, t):
        # 为每一个初始解计算t次
        vec_set = []
        m_set = []
        cost_set = []
        h = []
        for i in range(t):
            v, m, c, h = self.move(vec, h)
            vec_set.append(v)
            m_set.append(m)
            cost_set.append(c)
        return vec_set, m_set, cost_set

    def cacu_tiqu(self, v1, m1, c1):
        # 从上述t次筛选最小的解向量，移动和成本
        t = c1.index(min(c1))
        v_max = v1[t]
        m_max = m1[t]
        c_max = c1[t]
        return v_max, m_max, c_max

    def costroad(self, road):
        cost = 0
        for i in range(len(road) - 1):
            cost += self.dist[road[i], road[i+1]]
        cost += self.dist[0, road[0]]
        cost += self.dist[0, road[-1]]
        return cost
    def move(self, vec, h):  #输出移动后的向量，和成本
        i = 1
        while i == 1:
            m = random.sample(vec, 2)
            m.sort()
            if m not in h:
                h.append(m)
                vec_copy = vec[:]
                vec_copy[vec_copy.index(m[0])] = m[1]
                vec_copy[vec_copy.index(m[1])] = m[0]
                cost = self.costroad(vec_copy)
                i = 0
                return(vec_copy, m,cost, h)
    def _search_(self):
        print("The program now is executing...")
        start_time = time.time()
        finall_road = []
        finall_cost = []
        logs = []
        for t1 in range(self.origin_times):
            road = [i for i in range(1, self.city_nums)]
            random.shuffle(road)  # 打乱点数

            tabu_cost = []
            tabu_move = []
            for t in range(self.diedaitimes):
                i = 0
                while i == 0:
                    v1, m1, c1 = self.cacu(road, self.cacu_time)
                    v_m, m_m, c_m = self.cacu_tiqu(v1, m1, c1)
                    key1 = self.pan_move(m_m, tabu_move)  # 判断移动是否在禁忌表中
                    if key1[0]:
                        # 如果在，判断该移动是否比禁忌区域中该移动小，如果小则返回True，否则返回False
                        if self.pan_cost(c_m, tabu_cost, key1[1]):
                            # 如果小
                            road = v_m
                            finall_road.append(road)
                            finall_cost.append(c_m)
                            tabu_cost, tabu_move = self.add_tabu(c_m, m_m, tabu_cost, tabu_move, self.tabu_length)
                            i = 1
                        else:
                            # 否则
                            v1.remove(v_m)
                            m1.remove(m_m)
                            c1.remove(c_m)
                            if len(v1) == 0:
                                i = 1
                    else:
                        # 如果不在禁忌表中
                        tabu_cost, tabu_move = self.add_tabu(c_m, m_m, tabu_cost, tabu_move, self.tabu_length)
                        road = v_m
                        finall_road.append(road)
                        finall_cost.append(c_m)
                        i = 1
            ind = finall_cost.index(min(finall_cost))
            print("Iter:%d" % t1, "Total Distance: ", str(round(self.costroad(finall_road[ind]), 3)))
            logs.append(int(self.costroad(finall_road[ind])))

        index = finall_cost.index(min(finall_cost))
        over_time = time.time()
        path = finall_road[index]
        path.insert(0, 0)  # 插入固定的起始点
        path.append(0)  # 插入固定的回归点
        info = ["Tabu Search", str(self.origin_times) + " times", str(round(self.costroad(finall_road[index]), 3)) + " Km"]
        return path, info, over_time - start_time, logs