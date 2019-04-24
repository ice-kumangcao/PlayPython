"""
遗传算法求解2*sin(x) + cos(x)最大值

代码来源，python代码有些许问题
https://blog.csdn.net/quinn1994/article/details/80501542
参考
https://www.cnblogs.com/adelaide/articles/5679475.html
"""
import random
import math
import matplotlib.pyplot as plt


class GA:
    def __init__(self, population_length, chromosome_length, max_value, pc, pm):
        # 种群中个体数
        self.population_length = population_length
        # 一个染色体长度
        self.chromosome_length = chromosome_length
        self.max_value = max_value
        # 交叉概率
        self.pc = pc
        # 变异概率
        self.pm = pm

    # 初始化种群
    def species_origin(self):
        population = []
        for i in range(self.population_length):
            temporary = []
            for j in range(self.chromosome_length):
                temporary.append(random.randint(0, 1))
            population.append(temporary)
        return population[:]

    # 从二进制到十进制
    def translation(self, population):
        temporary = []
        for i in range(len(population)):
            total = 0
            for j in range(self.chromosome_length):
                total += population[i][j] * (math.pow(2, j))
            temporary.append(total)
        return temporary

    # 将染色体序列转换为x值 计算2*sin(x)+cos(x)结果
    def function(self, population):
        function1 = []
        temporary = self.translation(population)
        for i in range(len(temporary)):
            x = temporary[i] * self.max_value / (math.pow(2, self.chromosome_length) - 10)
            function1.append(2 * math.sin(x) + math.cos(x))
        return function1

    # 计算适应度
    def fitness(self, function1):
        fitness_value = []
        for i in range(len(function1)):
            if function1[i] > 0:
                temporary = function1[i]
            else:
                temporary = 0.0
            fitness_value.append(temporary)
        return fitness_value

    # 计算种群的总适应度
    def sum(self, fitness_value):
        total = 0
        for i in range(len(fitness_value)):
            total += fitness_value[i]
        return total

    def cumsum(self, fitness):
        for i in range(len(fitness) - 2, -1, -1):
            total = 0
            j = 0
            while j <= i:
                total += fitness[j]
                j += 1
            fitness[i] = total
        fitness[len(fitness) - 1] = 1

    # 轮盘法筛选个体
    def selection(self, population, fitness_value):
        new_fitness = []
        total_fitness = self.sum(fitness_value)
        for i in range(len(fitness_value)):
            new_fitness.append(fitness_value[i] / total_fitness)
        self.cumsum(new_fitness)
        ms = []
        pop_len = len(population)

        for i in range(pop_len):
            ms.append(random.random())
        fit_in = 0
        new_in = 0
        while new_in < pop_len:
            if ms[new_in] < new_fitness[fit_in]:
                population[new_in] = population[fit_in]
                new_in += 1
            else:
                fit_in += 1

    # 交叉操作
    def crossover(self, population):
        pop_len = len(population)
        for i in range(pop_len - 1):
            if random.random() < self.pc:
                cpoint = random.randint(0, len(population[i]))
                temp1 = []
                temp2 = []

                temp1.extend(population[i][:cpoint])
                temp1.extend(population[i + 1][cpoint:len(population[i])])

                temp2.extend(population[i + 1][:cpoint])
                temp2.extend(population[i][cpoint:len(population[i])])

                population[i] = temp1
                population[i + 1] = temp2

    # 变异
    def mutation(self, population):
        px = len(population)
        py = len(population[0])
        for i in range(px):
            if random.random() < self.pm:
                mpoint = random.randint(0, py - 1)
                if population[i][mpoint] == 1:
                    population[i][mpoint] = 0
                else:
                    population[i][mpoint] = 1

    # 将染色体映射x值
    def b2d(self, best_individual):
        total = 0
        for i in range(len(best_individual)):
            total += best_individual[i] * math.pow(2, i)

        total = total * self.max_value / (math.pow(2, self.chromosome_length) - 1)
        return total

    # 找到种群中适应度最高的个体
    def best(self, population, fitness_value):
        px = len(population)
        best_individual = []
        best_fitness = fitness_value[0]
        for i in range(1, px):
            if fitness_value[i] > best_fitness:
                best_fitness = fitness_value[i]
                best_individual = population[i]
        return [best_individual, best_fitness]

    # 绘出每次迭代中最优个体
    def plot(self, results):
        X = []
        Y = []
        for i in range(1000):
            X.append(i)
            Y.append(results[i][0])
        plt.plot(X, Y)
        plt.show()

    # 执行遗传算法
    def run(self):
        # 每次迭代中最优个体
        results = []
        # 初始化个体
        population = self.species_origin()

        for i in range(1000):
            # 计算适应度
            function_value = self.function(population)
            fitness_value = self.fitness(function_value)
            # 找到适应度最高的个体
            best_individual, best_fitness = self.best(population, fitness_value)
            results.append([best_fitness, self.b2d(best_individual)])
            # 选择
            self.selection(population, fitness_value)
            # 交叉
            self.crossover(population)
            # 变异
            self.mutation(population)
        results = results[:]
        results.sort()
        self.plot(results)


if __name__ == '__main__':
    population_size = 400
    max_value = 10
    chromosome_length = 20
    pc = 0.1
    pm = 0.6
    ga = GA(population_size, chromosome_length, max_value, pc, pm)
    ga.run()
