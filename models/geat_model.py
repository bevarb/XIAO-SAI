import numpy as np
import geatpy as ea
class MyProblem(ea.Problem): # 继承Problem父类
    def __init__(self, dist):
        name = 'Shortest_Path'  # 初始化name（函数名称，可以随意设置）
        M = 1  # 初始化M（目标维数）
        maxormins = [1]  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        Dim = 30  # 初始化Dim（决策变量维数）
        varTypes = [1] * Dim  # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [0] * Dim  # 决策变量下界
        ub = [29] * Dim  # 决策变量上界
        lbin = [1] * Dim  # 决策变量下边界
        ubin = [1] * Dim  # 决策变量上边界
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)
        # 设置每一个结点下一步可达的结点（结点从1开始数，因此列表nodes的第0号元素设为空列表表示无意义）
        self.nodes = []
        for i in range(Dim):
            temp = []
            for j in range(Dim):
                if j != i:
                    temp.append(j)
            self.nodes.append(temp)
        # 设置有向图中各条边的权重
        self.dist = dist

    def decode(self, priority):  # 将优先级编码的染色体解码得到一条从节点1到节点30的可行路径
        edges = []  # 存储边
        path = [0]  # 结点1是路径起点
        for i in range(30):  # 开始从起点走到终点
            currentNode = path[-1]  # 得到当前所在的结点编号
            nextNodes = self.nodes[currentNode].copy()  # 获取下一步可达的结点组成的列表
            for p in path:
                if p in nextNodes:
                    nextNodes.remove(p)
            if i == 29:
                nextNodes.append(0)
            #  从NextNodes中选择优先级更高的结点作为下一步要访问的结点，因为结点从1数起，而下标从0数起，因此要减去1
            chooseNode = nextNodes[np.argmax(priority[np.array(nextNodes)])]
            path.append(chooseNode)
            edges.append((currentNode, chooseNode))
        return path, edges
    def aimFunc(self, pop): # 目标函数
        pop.ObjV = np.zeros((pop.sizes, 1))  # 初始化ObjV
        for i in range(pop.sizes):
            priority = pop.Phen[i, :]
            path, edges = self.decode(priority)  # 将优先级编码的染色体解码得到访问路径及经过的边
            pathLen = 0
            for edge in edges:

                pathLen += self.dist[edge[0], edge[1]]  # 将该段路径长度加入
            # err = (30 - len(path)) * 300
            pop.ObjV[i] = pathLen  # 计算目标函数值，赋值给pop种群对象的ObjV属性
