import tkinter as tk
import numpy as np
import random as rd


class GameOfLife():
    def __init__(self, data):
        self.name = 'game of life'
        self.width = 600
        self.height = 550
        self.window = tk.Tk()
        self.window.title(self.name)
        self.window.geometry('{}x{}'.format(self.width, self.height))
        self.canvas = tk.Canvas(self.window, bg='white', width=self.width-100, height=self.height-50 )
        self.array = np.zeros((int((self.width-100)/20), int((self.height-50)/20)), dtype=int)
        self.start_btn = tk.Button(self.window, bg='gray', text='start',command=self.start)
        self.pause_btn = tk.Button(self.window, bg='gray', text='pause',command=self.pause)
        self.refresh_btn = tk.Button(self.window, bg='gray', text='clear',command=self.restart)
        self.quit_btn = tk.Button(self.window, bg='gray', text='quit',command=self.window.quit)
        self.Step_Label = tk.Label(self.window, bg="gray", text="Step:")
        self.data = data  # 存放排列
        self.central_x, self.central_y = self.array.shape[0] // 2, self.array.shape[1] // 2
        # 设置暂停标志
        self.flag = 0
        # 设置start次数，防止加速
        self.count = 0
        self.step = 0  # 设置步数



    def pack(self):
        self.canvas.pack()
        self.start_btn.place(x=10, y=self.height - 30, anchor='nw')
        self.pause_btn.place(x=150, y=self.height - 30, anchor='nw')
        self.refresh_btn.place(x=290, y=self.height - 30, anchor='nw')
        self.quit_btn.place(x=430, y=self.height - 30, anchor='nw')
        self.Step_Label.place(x=10, y=30, anchor="nw")

    def init_cells(self):
        count = 0
        self.step = 0
        self.array = self.array * 0
        if self.data.any() != None:
            # 按照data排列组合产生
            shape = self.data.shape
            begain_x, begain_y = self.central_x - shape[0] // 2, self.central_y - shape[1] // 2
            self.array[begain_x: begain_x + shape[0], begain_y:begain_y + shape[1]] = self.data
        else:
            #  随机产生细胞
            for x in range(len(self.array)):
                for y in range(len(self.array[x])):
                    if count > 200:
                        return
                    if rd.randint(0, 100) >= 50:
                        self.array[x][y] = 1
                        count += 1

    def draw(self):
        # 画图
        for i in range(len(self.array)):
            for j in range(len(self.array[i])):
                if self.array[i][j] == 1:
                    self.canvas.create_oval(j*20, i*20, j*20+20, i*20+20, fill='black')
                else:
                    self.canvas.create_rectangle(j * 20, i * 20, j * 20 + 20, i * 20 + 20, fill='white')
        self.Step_Label["text"] = "Step:%d" % self.step

    def start(self):
        if self.flag == 1:
            return
        self.flag = 1
        self.refresh()

    def pause(self):
        print("Have Paused!")
        self.flag = 0

    def refresh(self):
        if self.flag == 1:
            for i in range(1, len(self.array) - 1):
                for j in range(1, len(self.array[i]) - 1):
                    sum = self.array[i][j - 1] + self.array[i - 1][j - 1] + self.array[i - 1][j] + self.array[i - 1][
                        j + 1] + self.array[i][j + 1] + self.array[i + 1][j + 1] + self.array[i + 1][j] + self.array[i + 1][ j - 1]

                    # 活细胞
                    if self.array[i][j] == 1:
                        if sum != 2 and sum != 3:
                            self.array[i][j] = 0
                    # 死细胞
                    else:
                        if sum == 3:
                            self.array[i][j] = 1
            self.step += 1
            self.draw()
            self.canvas.after(500, self.refresh)
        else:
            return

    def restart(self):
        print("Have Restarted!")
        self.flag = 0
        self.init_cells()
        self.draw()
        self.pause()


    def show(self):
        self.canvas.mainloop()


if __name__ == '__main__':
    data = np.array([
        [0, 1, 1],
        [0, 1, 1],
        [0, 1, 1]]
    )
    game1 = GameOfLife(data=data)  # 初始化
    game1.pack()  #
    game1.init_cells()
    game1.draw()
    game1.show()