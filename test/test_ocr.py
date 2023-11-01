from paddleocr import PaddleOCR, draw_ocr
from PIL import Image, ImageDraw
from shapely.geometry import Polygon


def get_ocr(cv_image):   # input:image   output:[[[int,int],[int,int],[int,int],[int,int]],(character,float)]
    pre_ocr = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=False)
    cv_result = pre_ocr.ocr(cv_image, cls=True)

    # 将所有坐标存放在rectangles
    rectangles = []
    for index in range(len(cv_result)):
        contant = result[index]
        for sth in contant:
            rectangles.append(sth)

    return rectangles


if __name__ == '__main__':
    # Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
    # 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
    # obj = 'altman'
    # obj = 'area_chart'
    # obj = 'bar_chart'
    # obj = 'customer_seq'
    # obj = 'flow_chart'
    # obj = 'formula'
    # obj = 'knowledge'
    # obj = 'line_chart'
    # obj = 'prompt'
    # obj = 'teach'
    # obj = 'triangle'
    objs = [
        'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11',
        'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F16',
        'J5', 'J6', 'J12',
        'N3'
    ]
    for obj in objs:
        img_path = f'../pic/{obj}.png'
        result = ocr.ocr(img_path, cls=True)
        polygons = []
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                # print(line)
                polygons.append(Polygon(line[0]))

        # 获取图片的高度和宽度
        image = Image.open(img_path)
        width, height = image.size
        # width = 1920
        # height = 1080

        im = Image.new('RGBA', (width, height), (255, 255, 255))
        gdi = ImageDraw.Draw(im)
        for po in polygons:
            # 将多边形绘制到图像上
            exterior_coords = list(po.exterior.coords)
            gdi.polygon(exterior_coords, outline="black", fill="blue")
        im.save(f'../output/{obj}.png', )
        # 显示结果
        result = result[0]
        image = Image.open(img_path).convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
        im_show = Image.fromarray(im_show)
        im_show.save(f'../output/{obj}.png')
