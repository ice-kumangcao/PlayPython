"""
蚁群算法解决TSP问题
"""
import random
import sys
import tkinter
import threading
import copy
from functools import reduce

'''
ALPHA:信息启发因子，值越大，则蚂蚁选择之前走过的路径可能性就越大
      ，值越小，则蚁群搜索范围就会减少，容易陷入局部最优
BETA:Beta值越大，蚁群越就容易选择局部较短路径，这时算法收敛速度会
     加快，但是随机性不高，/home/ice/Desktop/高二/2_18-19第二学期高二年级排课需求(1)(1).docx
'''

(ALPHA, BETA, RHO, Q) = (1.0, 2.0, 0.5, 100.0)
# 城市数，蚁群
(city_num, ant_num) = (50, 50)

distance_x = [
    178, 272, 176, 171, 650, 499, 267, 703, 408, 437, 491, 74, 532,
    416, 626, 42, 271, 359, 163, 508, 229, 576, 147, 560, 35, 714,
    757, 517, 64, 314, 675, 690, 391, 628, 87, 240, 705, 699, 258,
    428, 614, 36, 360, 482, 666, 597, 209, 201, 492, 294]
distance_y = [
    170, 395, 198, 151, 242, 556, 57, 401, 305, 421, 267, 105, 525,
    381, 244, 330, 395, 169, 141, 380, 153, 442, 528, 329, 232, 48,
    498, 265, 343, 120, 165, 50, 433, 63, 491, 275, 348, 222, 288,
    490, 213, 524, 244, 114, 104, 552, 70, 425, 227, 331]

# 城市距离和信息素
distance_graph = [[0.0 for col in range(city_num)] for raw in range(city_num)]
pheromone_graph = [[1.0 for col in range(city_num)] for raw in range(city_num)]


class Ant:

    def __init__(self, id):
        self.id = id
        self.__clean_data()

    def __clean_data(self):
        self.path = []  # 当前蚂蚁的路径
        self.total_distance = 0.0  # 当前路径的总距离
        self.move_count = 0  # 移动次数
        self.current_city = -1  # 当前停留的城市
        self.open_table_city = [True for i in range(city_num)]  # 探索城市的状态

        city_index = random.randint(0, city_num - 1)  # 随机初始出生点
        self.current_city = city_index
        self.path.append(city_index)
        self.open_table_city[city_index] = False
        self.move_count = 1

    # 选择下一个城市
    def __choice_next_city(self):
        next_city = -1
        select_citys_prob = [0.0 for i in range(city_num)]
        total_prob = 0.0

        # 获取下一个城市的概率
        for i in range(city_num):
            if self.open_table_city[i]:
                try:
                    # 计算概率：与信息素浓度成正比，与距离成反比
                    select_citys_prob[i] = pow(pheromone_graph[self.current_city][i], ALPHA) * pow(
                        (1.0 / distance_graph[self.current_city][i]), BETA)
                    total_prob += select_citys_prob[i]
                except ZeroDivisionError as e:
                    print('And id :{id},current city: {current}, target city: {target}'.
                          format(id=self.id, current=self.current_city, target=i))
                    sys.exit(1)

        # 轮盘选择城市
        if total_prob > 0.0:
            # 产生一个随机概率, 0 - total_prob
            temp_prob = random.uniform(0.0, total_prob)
            for i in range(city_num):
                if self.open_table_city[i]:
                    # 轮次相减
                    temp_prob -= select_citys_prob[i]
                    if temp_prob < 0.0:
                        next_city = i
                        break

        if next_city == -1:
            next_city = random.randint(0, city_num - 1)
            while not self.open_table_city[next_city]:
                next_city = random.randint(0, city_num - 1)

        # 返回下一个城市序号
        return next_city

    # 计算路径总距离
    def __cal_total_distance(self):
        temp_distance = 0.0
        for i in range(1, city_num):
            start, end = self.path[i], self.path[i - 1]
            temp_distance += distance_graph[start][end]

        # 回路
        end = self.path[0]
        temp_distance += distance_graph[start][end]
        self.total_distance = temp_distance

    # 移动操作
    def __move(self, next_city):

        self.path.append(next_city)
        self.open_table_city[next_city] = False
        self.total_distance += distance_graph[self.current_city][next_city]
        self.current_city = next_city
        self.move_count += 1

    # 搜索路径
    def search_path(self):
        # 初始化数据
        self.__clean_data()

        # 搜索路径，遍历完所有城市为止
        while self.move_count < city_num:
            # 移动到下一个城市
            next_city = self.__choice_next_city()
            self.__move(next_city)

        # 计算路径总长度
        self.__cal_total_distance()


class TSP:

    def __init__(self, root, width=800, height=600, n=city_num):
        # 创建画布
        self.root = root
        self.width = width
        self.height = height
        self.n = n
        self.canvas = tkinter.Canvas(root,
                                     width=self.width,
                                     height=self.height,
                                     bg="#EBEBEB",
                                     xscrollincrement=1,
                                     yscrollincrement=1)
        self.canvas.pack(expand=tkinter.YES, fill=tkinter.BOTH)
        self.title("TSP蚁群算法(n:初始化 e:开始搜索 s:停止搜索 q:退出程序)")
        self.__r = 5
        self.__lock = threading.RLock()

        self.__bind_events()
        self.new()

        for i in range(city_num):
            for j in range(city_num):
                temp_distance = pow((distance_x[i] - distance_x[j]), 2) + pow((distance_y[i] - distance_y[j]), 2)
                temp_distance = pow(temp_distance, 0.5)
                distance_graph[i][j] = float(int(temp_distance + 0.5))

    def __bind_events(self):
        self.root.bind("q", self.quite)
        self.root.bind("n", self.new)
        self.root.bind("e", self.search_path)
        self.root.bind('s', self.stop)

    def title(self, s):
        self.root.title(s)

    def new(self, evt=None):
        # 停止线程
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()

        self.clear()
        self.nodes = []
        self.nodes2 = []

        for i in range(len(distance_x)):
            x = distance_x[i]
            y = distance_y[i]
            self.nodes.append((x, y))
            node = self.canvas.create_oval(x - self.__r, y - self.__r,
                                           x + self.__r, y + self.__r,
                                           fill='#ff0000', outline='#000000', tags='node')
            self.nodes2.append(node)

            self.canvas.create_text(x, y - 10,
                                    text='(' + str(x) + ', ' + str(y) + ')',
                                    fill='black')

        for i in range(city_num):
            for j in range(city_num):
                pheromone_graph[i][j] = 1.0

        self.ants = [Ant(id) for id in range(ant_num)]
        self.best_ant = Ant(-1)
        self.best_ant.total_distance = 1 << 31
        self.iter = 1

    def line(self, order):
        self.canvas.delete('line')

        def line2(i1, i2):
            p1, p2 = self.nodes[i1], self.nodes[i2]
            self.canvas.create_line(p1, p2, fill='#000000', tags='line')
            return i2

        reduce(line2, order, order[-1])

    def clear(self):
        for item in self.canvas.find_all():
            self.canvas.delete(item)

    def quite(self, evt):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()
        self.root.destroy()
        print('\n程序已退出...')
        sys.exit()

    def stop(self, evt):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()

    def search_path(self, evt=None):
        self.__lock.acquire()
        self.__running = True
        self.__lock.release()

        while self.__running:
            for ant in self.ants:
                ant.search_path()
                if ant.total_distance < self.best_ant.total_distance:
                    self.best_ant = copy.deepcopy(ant)
            self.__update_pheromone_graph()
            print('迭代次数:', self.iter, '最佳路径总距离:', int(self.best_ant.total_distance))
            self.line(self.best_ant.path)
            self.title("TSP蚁群算法(n:随机初始 e:开始搜索 s:停止搜索 q:退出程序) 迭代次数: %d" % self.iter)

            self.canvas.update()
            self.iter += 1

    def __update_pheromone_graph(self):
        temp_pheromone = [[0.0 for col in range(city_num)] for raw in range(city_num)]
        for ant in self.ants:
            for i in range(1, city_num):
                start, end = ant.path[i - 1], ant.path[i]
                temp_pheromone[start][end] += Q / ant.total_distance
                temp_pheromone[end][start] = temp_pheromone[start][end]

        for i in range(city_num):
            for j in range(city_num):
                pheromone_graph[i][j] = pheromone_graph[i][j] * RHO + temp_pheromone[i][j]

    def main_loop(self):
        self.root.mainloop()


if __name__ == '__main__':
    TSP(tkinter.Tk()).main_loop()
