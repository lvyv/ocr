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
import glob
import os
import cv2
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image, ImageDraw, ImageFont
from app import __version__

# 配置logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s %(filename)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S')


def get_ocr(image):
    # input:image   output:[[[int,int],[int,int],[int,int],[int,int]],(character,float)]
    ocr = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=False)
    result = ocr.ocr(image, cls=True)

    # 将所有坐标存放在rectangles
    rectangles = []
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            rectangles.append(line)

    return rectangles


def get_image_and_ocr_and_result(file):
    res = None
    try:
        image = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)
        res = get_ocr(image)
        logger.info(f'1. OCR ended.')
    finally:
        return res


def read_image(image_path):
    # 打开图片文件并读取字节流
    res = None
    try:
        with open(image_path, 'rb') as file:
            res = file.read()
            logger.info("成功读取图像文件的字节流")
    except FileNotFoundError:
        logger.error(f"找不到文件：{image_path}")
    except Exception as e:
        logger.error(f"发生错误：{e}")
    finally:
        return res


def label_image(infile, outfile, labels):
    # 1. 打开已有的图片文件
    input_image = Image.open(infile)  # 将路径替换为你的输入图片文件路径

    # 2. 标注图像
    # 创建一个绘图对象
    draw = ImageDraw.Draw(input_image)
    # 在图片上绘制矩形，文本，置信度
    font = ImageFont.truetype('../fonts/cf.ttf', size=24)  # 使用指定字体和大小
    text_color = (255, 0, 0)  # 红色 (R, G, B)
    ocr_results = []
    # paddleOCR识别结果为若干的[[],()]对象，列表前一个元素是4个点组成的矩形，后一个元组为识别的文字和置信度
    for lbl in labels:
        rect = lbl[0]
        text = lbl[1][0]
        confident = lbl[1][1]
        text = f'{text}({confident:.2f})\t' + str(rect) # 用\t方便后面分割
        text_position = (rect[0][0], rect[0][1])
        draw.text(text_position, text, fill=text_color, font=font)
        polygon_points = [tuple(lst) for lst in rect]
        draw.polygon(polygon_points, outline='red', width=2)
        ocr_results.append(text)
    # 3. 保存绘制后的图片为另外的文件，并把识别结果保存为一个txt文件
    input_image.save(outfile)
    file_path = outfile+'.txt'
    with open(file_path, "w", encoding="utf-8") as file:
        for result in ocr_results:
            # 写入每个元素并在末尾添加换行符
            file.write(result + "\n")


def findFiles(path):
    return glob.glob(path)


def test_version():
    assert __version__ == "0.1.0"


class TestMain(unittest.TestCase):
    """
    Tests for `ocr` 标记
    本测试案例启动ocr图片的标记
    """
    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_img_deal(self):
        logger.info(f'Begin picture processing procedure testing...')
        objs = [
            'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11',
            'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F16',
            'J5', 'J6', 'J12',
            'N3'
        ]
        for obj in objs:
            filename = f'../pic/{obj}.png'
            file = read_image(filename)
            res = get_image_and_ocr_and_result(file)
            label_image(filename, f'../output/{os.path.basename(filename)}', res)
            # self.assertIn('error', res, 'error in result')


if __name__ == "__main__":
    unittest.main()
