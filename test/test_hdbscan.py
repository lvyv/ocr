import numpy as np
from sklearn.cluster import HDBSCAN
from collections import Counter


def produce_point(rectangle):

    # ��ȡ���ε����½Ǻ����Ͻ�����
    bottom_left = rectangle[0]
    top_right = rectangle[2]

    # ���������
    points = np.mgrid[bottom_left[0]:top_right[0]+1:20, bottom_left[1]:top_right[1]+1:20].reshape(2, -1).T

    return points


def get_merged_polygon_for_hdbscan(rectangles):   # output:[[ͬһ���������],[]]
    # ����������ת��Ϊ�������� features
    # ����һ���ֵ� chara = {�����֡����������ɵĵ�ĸ���}
    chara = {}
    features = np.array([[0, 0]])
    for rectangle in rectangles:
        points = produce_point(rectangle[0])
        chara[rectangle[1][0]] = len(points)
        features = np.append(features, points, axis=0)

    # ����hdbscanģ�Ͳ�ѵ���õ�labels
    hdb = HDBSCAN()
    hdb.fit(features)
    labels = hdb.labels_

    # ��ÿ�������е����ֺϲ���һ��
    characters = {}
    now_node = 1
    for wenzi in chara.keys():
        nums = chara[wenzi]
        wz_labels = Counter(labels[now_node:now_node + nums])  # wz_labels��ʾ���������ڵľ��������ɵĵ������Ӧ�ı�ǩ��ͳ�Ƶ�����
        now_node += nums

        # �ҵ����ı�ǩ
        max_label = 0
        max_label_num = 0
        for i in wz_labels:
            if wz_labels[i] > max_label_num:
                max_label = i
                max_label_num = wz_labels[i]

        if max_label not in characters:
            characters[max_label] = []
        characters[max_label].append(wenzi)

    # ��ÿ����������ִ�ŵ��б���
    final = []
    for i in characters.keys():
        final.append(characters[i])

    return final
