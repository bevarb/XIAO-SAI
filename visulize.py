import cv2 as cv
from PIL import Image, ImageDraw, ImageFont
import numpy as np
class visulize():
    def base_map(self, real_data):
        '''可视化基本地图，将原来的点放大两倍，左下角为坐标原点，左->右为x轴，右->左为y轴
        将原来的点除以5，放缩一下基本像素点为5KM
        '''
        img = Image.fromarray(np.zeros((550, 550, 3), dtype=np.uint8) + 255)
        real_data[:, 0:2] = real_data[:, 0:2] / 10
        new_data = []  # 把新的位置重新定义下， 可以根据索引画线
        for i in range(len(real_data)):
            new_data.append([int(real_data[i][0] * 2 + 45), int(550 - real_data[i][1] * 2 - 55), i])
        # 两个贴图
        DC = Image.fromarray(cv.resize(cv.imread("icon/DC.png"), (30, 20)))
        sensor = Image.fromarray(cv.resize(cv.imread("icon/sensor.png"), (20, 15)))
        # 将贴图放上去
        for i in range(len(real_data)):
            if i == 0:
                img.paste(DC, (new_data[i][0], new_data[i][1]))
            else:
                img.paste(sensor, (new_data[i][0], new_data[i][1]))
        # 标签放上去
        font = ImageFont.truetype(font='msyh.ttf', size=10)
        draw = ImageDraw.ImageDraw(img)
        for i in range(len(real_data)):
            if i == 0:
                draw.text((new_data[i][0] + 8, new_data[i][1] + 20), "DC", "black", font=font)
            else:
                draw.text((new_data[i][0] - 10, new_data[i][1] + 15), "sensor%d" % i, "black", font=font)
        draw.line((480, 50, 490, 50), "black")
        draw.line((480, 48, 480, 50), "black")
        draw.line((490, 48, 490, 50), "black")
        draw.text((500, 40), "50Km", "black", font=ImageFont.truetype(font='msyh.ttf', size=10))
        cv.imwrite("baseMap.png", np.array(img))