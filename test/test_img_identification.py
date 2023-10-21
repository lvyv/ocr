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
from PIL import Image, ImageDraw, ImageFont
from app import __version__
from app.main import get_image_and_ocr_and_result

# 配置logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s %(filename)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S')


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
    # paddleOCR识别结果为若干的[[],()]对象，列表前一个元素是4个点组成的矩形，后一个元组为识别的文字和置信度
    for lbl in labels:
        rect = lbl[0]
        text = lbl[1][0]
        confident = lbl[1][1]
        text = f'{text}({confident:.2f})'
        text_position = (rect[0][0], rect[0][1])
        draw.text(text_position, text, fill=text_color, font=font)
        polygon_points = [tuple(lst) for lst in rect]
        draw.polygon(polygon_points, outline = 'red', width = 2)

    # 3. 保存绘制后的图片为另外的文件
    input_image.save(outfile)


def findFiles(path):
    return glob.glob(path)


def test_version():
    assert __version__ == "0.1.0"


class TestMain(unittest.TestCase):
    """
    Tests for `健康模型构件` entrypoint.
    本测试案例启动整个健康模型构件（可以在数据资源集成分系统的算法开发软件中部署的模型协同工作）
    访问运行本案例的URL：
    https://IP:29081/docs，执行POST /subprocess，发送start/stop命令启停视频识别流水线。
    注意
    """
    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_img_deal(self):
        logger.info(f'Begin picture processing procedure testing...')
        for filename in findFiles('../pic/important-*.png'):
            file = read_image(filename)
            res = get_image_and_ocr_and_result(file)
            label_image(filename, f'out/{os.path.basename(filename)}', res[0])
            # self.assertIn('error', res, 'error in result')


if __name__ == "__main__":
    unittest.main()
