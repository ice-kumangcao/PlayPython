"""
k-means算法
"""
import random
import math


class KMeans:

    def __init__(self):
        self.num_of_cluster = 4
        self.time_of_iteration = 20
        self.point_length = 2
        self.data_set = []
        self.centers = []
        self.clusters = []
        self.sum_of_error_square = 0

    def init_data_set(self, data_set):
        self.data_set = data_set

    def init_centers(self, centers=None):
        if centers is None:
            self.centers = random.sample(self.data_set, self.num_of_cluster)
        else:
            self.num_of_cluster = len(self.centers)

    @staticmethod
    def _distance(element, center):
        return math.sqrt((element[0] - center[0]) ** 2 + (element[1] - center[1]) ** 2)

    def _min_distance(self, element):
        distances = [self._distance(element, center) for center in self.centers]
        return distances.index(min(distances))

    def new_center(self):
        new_centers = []
        for cluster in self.clusters:
            new_center_sum = [0.0 for x in range(self.point_length)]
            for point in cluster:
                for i in range(self.point_length):
                    new_center_sum += point[i]
            new_center = [x / len(cluster) for x in new_center_sum]
            new_centers.append(new_center)
        return new_centers

    def _cluster_data_set(self):
        self.clusters = [[] for x in range(self.num_of_cluster)]
        for element in self.data_set:
            index = self._min_distance(element)
            self.clusters[index].append(element)
        new_centers = self.new_center()
        self.centers = new_centers

    def run(self):
        for x in range(self.time_of_iteration):
            self._cluster_data_set()
