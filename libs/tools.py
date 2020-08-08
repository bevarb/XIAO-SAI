import math
import numpy as np
def millerToXY(lon, lat):
    """
    :param lon: 经度
    :param lat: 维度
    :return:
    """
    L = 6381372 * math.pi * 2  # 地球周长
    W = L  # 平面展开，将周长视为X轴
    H = L / 2  # Y轴约等于周长一般
    mill = 2.3  # 米勒投影中的一个常数，范围大约在正负2.3之间
    x = lon * math.pi / 180  # 将经度从度数转换为弧度
    y = lat * math.pi / 180  # 将纬度从度数转换为弧度
    y = 1.25 * math.log(math.tan(0.25 * math.pi + 0.4 * y))  # 这里是米勒投影的转换

    # 这里将弧度转为实际距离 ，转换结果的单位是公里
    x = (W / 2) + (W / (2 * math.pi)) * x
    y = (H / 2) - (H / (2 * mill)) * y

    return int(round(x)), int(round(y))

def get_dist(point1, point2):
    dist = np.sqrt(np.square(point1[0] - point2[0]) + np.square(point1[1] - point2[1]))
    return dist