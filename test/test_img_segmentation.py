#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2021 The Xiaobu Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
# pylint: disable=invalid-name
# pylint: disable=missing-docstring

"""
=========================
unit test module
=========================

测试模型调度核心模块的入口主进程.
"""

# Author: Awen <26896225@qq.com>
# License: MIT

import unittest
import logging
import cv2
import matplotlib.pyplot as plt
import numpy as np
from sam import SAMwrapper
from app import __version__


# 配置logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s %(filename)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S')


def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)


def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels == 1]
    neg_points = coords[labels == 0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white',
               linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white',
               linewidth=1.25)


def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0, 0, 0, 0), lw=2))


def test_version():
    assert __version__ == "0.1.0"


class TestMain(unittest.TestCase):
    """
    Tests for `ocr` 标记
    本测试案例启动ocr图片的标记
    """
    def setUp(self):
        """Set up test fixtures, if any."""
        self.sam_ = SAMwrapper('vit_h', 'E:\\_proj\\segment-anything\\checkpoints\\sam_vit_h_4b8939.pth')

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_img_segmentation(self):
        logger.info(f'Begin picture processing procedure testing...')
        objs = [
            'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11',
            'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F16',
            'J5', 'J6', 'J12',
            'N3'
        ]
        for obj in objs:
            filename = f'../pic/{obj}.png'
            image = cv2.imread(filename)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            points = [[34.0, 33.0], [1061.0, 33.0], [1061.0, 96.0], [34.0, 96.0]]
            masks, scores, logits = self.sam_.predict_mask(image, points)

            for i, (mask, score) in enumerate(zip(masks, scores)):
                plt.figure()
                plt.imshow(image)
                show_mask(mask, plt.gca())
                input_point = np.array(points)
                input_label = np.array([1 for _ in range(len(points))])
                show_points(input_point, input_label, plt.gca())
                plt.title(f"Mask {i+1}, Score: {score:.3f}", fontsize=18)
                plt.axis('off')
                plt.show()


if __name__ == "__main__":
    unittest.main()
