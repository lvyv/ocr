import numpy as np
from sklearn.cluster import HDBSCAN
from collections import Counter


def produce_point(rectangle):

    # 提取矩形的左下角和右上角坐标
    bottom_left = rectangle[0]
    top_right = rectangle[2]

    # 生成坐标点
    points = np.mgrid[bottom_left[0]:top_right[0]+1:20, bottom_left[1]:top_right[1]+1:20].reshape(2, -1).T

    return points


def get_merged_polygon_for_hdbscan(rectangles):   # output:[[同一聚类的文字],[]]
    # 将矩形坐标转换为特征向量 features
    # 创建一个字典 chara = {’文字’：矩形生成的点的个数}
    chara = {}
    features = np.array([[0, 0]])
    for rectangle in rectangles:
        points = produce_point(rectangle[0])
        chara[rectangle[1][0]] = len(points)
        features = np.append(features, points, axis=0)

    # 建立hdbscan模型并训练得到labels
    hdb = HDBSCAN()
    hdb.fit(features)
    labels = hdb.labels_

    # 将每个聚类中的文字合并到一起
    characters = {}
    now_node = 1
    for wenzi in chara.keys():
        nums = chara[wenzi]
        wz_labels = Counter(labels[now_node:now_node + nums])  # wz_labels表示在文字所在的矩形内生成的点个个对应的标签所统计的数量
        now_node += nums

        # 找到最多的标签
        max_label = 0
        max_label_num = 0
        for i in wz_labels:
            if wz_labels[i] > max_label_num:
                max_label = int(i)
                max_label_num = wz_labels[i]

        if max_label not in characters:
            characters[max_label] = []
        characters[max_label].append(wenzi)

    # 将每个聚类的文字存放到列表中
    final = []
    for i in characters.keys():
        final.append(characters[i])

    return characters
