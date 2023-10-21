from paddleocr import PaddleOCR, draw_ocr
from PIL import Image, ImageDraw
from shapely.geometry import Polygon


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

