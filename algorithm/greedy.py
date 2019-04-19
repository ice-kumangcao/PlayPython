"""
贪心算法-完全背包问题
"""
import time


class Goods:
    def __init__(self, good_id, weight=0, value=0):
        self.good_id = good_id
        self.weight = weight
        self.value = value


def knapsack(capacity=0, goods_set=[]):
    # 按单位价值量排序
    goods_set.sort(key=lambda obj: obj.value / obj.weight, reverse=True)
    result = []
    for goods in goods_set:
        if capacity < goods.weight:
            break
        result.append(goods)
        capacity -= goods.weight
    if len(result) < len(goods_set) and capacity != 0:
        result.append(Goods(goods.good_id, capacity, goods.value * capacity / goods.weight))
    return result


some_goods = [Goods(0, 2, 4), Goods(1, 8, 6), Goods(2, 5, 3), Goods(3, 2, 8), Goods(4, 1, 2)]

start_time = time.time()
result = knapsack(6, some_goods)
end_time = time.time()
print('time:', str(end_time - start_time))
for goods in result:
    print('id:', str(goods.good_id), 'weight:', str(goods.weight), 'value:', str(goods.value),
          '价值量:', str(goods.value / goods.weight))
