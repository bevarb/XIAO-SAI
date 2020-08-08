import pandas as pd
import numpy as np
from libs.visulize import visulize
from models.geat_model import MyProblem
import geatpy as ea
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
    vi.base_map(real_data)
    dist = np.zeros((30, 30), np.uint8)
    for i in range(len(real_data)):
        for j in range(len(real_data)):
            dist[i][j] = get_dist(real_data[i], real_data[j])

    problem = MyProblem(dist)                      # 生成问题对象
    """=================================种群设置================================="""
    Encoding = 'P'                             # 编码方式
    NIND = 500                                   # 种群规模
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
    population = ea.Population(Encoding, Field, NIND)  # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
    """===============================算法参数设置==============================="""
    myAlgorithm = ea.soea_SEGA_templet(problem, population)  # 实例化一个算法模板对象
    myAlgorithm.MAXGEN = 300                  # 最大进化代数
    myAlgorithm.recOper = ea.Xovox(XOVR=0.8)  # 设置交叉算子
    myAlgorithm.mutOper = ea.Mutinv(Pm=0.5)  # 设置变异算子
    myAlgorithm.drawing = 1                    # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制过程动画）
    """==========================调用算法模板进行种群进化=========================="""
    [population, obj_trace, var_trace] = myAlgorithm.run()  # 执行算法模板，得到最后一代种群以及进化记录器
    population.save()                          # 把最后一代种群的信息保存到文件中
    # 输出结果
    best_gen = np.argmin(obj_trace[:, 1])      # 记录最优种群是在哪一代
    best_ObjV = np.min(obj_trace[:, 1])
    print('最短路程为：%s'%(best_ObjV))
    print('最佳路线为：')
    best_journey, edges = problem.decode(var_trace[best_gen, :])
    print(best_journey)
    for i in range(len(best_journey)):
        print(int(best_journey[i]), end=' ')
    print()
    print('有效进化代数：%s'%(obj_trace.shape[0]))
    print('最优的一代是第 %s 代'%(best_gen + 1))
    print('评价次数：%s'%(myAlgorithm.evalsNum))
    print('时间已过 %s 秒'%(myAlgorithm.passTime))



