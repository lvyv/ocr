from multiprocessing import Queue

img_queue = Queue()  # 接收id和image
ocr_queue = Queue()  # 接收rectangles
