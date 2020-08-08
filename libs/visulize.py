import cv2 as cv
from PIL import Image, ImageDraw, ImageFont
import numpy as np
class visulize():
    def base_map(self, real_data):
        '''可视化基本地图，将原来的点放大两倍，左下角为坐标原点，左->右为x轴，右->左为y轴
        将原来的点除以5，放缩一下基本像素点为5KM
        '''
        img = Image.fromarray(np.zeros((750, 800, 3), dtype=np.uint8) + 255)
        real_data[:, 0:2] = real_data[:, 0:2] / 10
        self.new_data = []  # 把新的位置重新定义下， 可以根据索引画线
        for i in range(len(real_data)):
            self.new_data.append([int(real_data[i][0] * 2.7 + 20), int(550 - real_data[i][1] * 2.9) + 140, i])
        # 两个贴图
        DC = Image.fromarray(cv.resize(cv.imread("icon/DC.png"), (30, 20)))
        sensor = Image.fromarray(cv.resize(cv.imread("icon/sensor.png"), (20, 15)))
        # 将贴图放上去
        for i in range(len(real_data)):
            if i == 0:
                img.paste(DC, (self.new_data[i][0], self.new_data[i][1]))
            else:
                img.paste(sensor, (self.new_data[i][0], self.new_data[i][1]))
        # 标签放上去
        self.font = ImageFont.truetype(font='msyh.ttf', size=10)
        draw = ImageDraw.ImageDraw(img)
        for i in range(len(real_data)):
            if i == 0:
                draw.text((self.new_data[i][0] + 8, self.new_data[i][1] + 20), "DC", "black", font=self.font)
            else:
                draw.text((self.new_data[i][0] - 10, self.new_data[i][1] + 15), "sensor%d" % i, "black", font=self.font)
        draw.line((680, 50, 694, 50), "black")  # 横线
        draw.line((680, 48, 680, 50), "black")  # 竖线1
        draw.line((694, 48, 694, 50), "black")  # 竖线2
        draw.text((704, 40), "50Km", "black", font=ImageFont.truetype(font='msyh.ttf', size=10))
        cv.imwrite("baseMap.png", np.array(img))
        return img

    def arrow_map(self, base_map, path, info):
        """TODO:后面增加到4辆车，应该会有4个路径，格式应该在path里面放四个列表"""
        img = base_map.copy()
        draw = ImageDraw.ImageDraw(img)
        current_x, current_y = self.new_data[path[0]][0] + 15, self.new_data[path[0]][1] + 10
        next_x, next_y = self.new_data[path[1]][0] + 10, self.new_data[path[1]][1] + 6
        draw.line((current_x, current_y, next_x, next_y), "red", width=3)
        for i in range(1, len(path) - 1):
            current_x, current_y = next_x, next_y
            next_x, next_y = self.new_data[path[i + 1]][0] + 10, self.new_data[path[i + 1]][1] + 6
            draw.line((current_x, current_y, next_x, next_y), "red", width=3)

        draw.text((20, 20), "Method:", "black", font=self.font)
        draw.text((20, 35), "Total Iter:", "black", font=self.font)
        draw.text((20, 50), "Total Distance:", "black", font=self.font)
        draw.text((80, 20), info[0], "black", font=self.font)
        draw.text((80, 35), info[1], "black", font=self.font)
        draw.text((95, 50), info[2], "black", font=self.font)
        cv.imshow("Root", np.array(img))
        cv.waitKey()
