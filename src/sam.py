# 使用sam生成标签张量
# input: image: np.ndarray   output:masks

from segment_anything import SamAutomaticMaskGenerator, sam_model_registry, SamPredictor
# import cv2
import numpy as np
import config.constants as ct
import torch


def show_anns(anns):  # 构建标签张量
    if len(anns) == 0:
        return

    # 按照面积降序对注释进行排序
    sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)

    # 创建一个初始化张量
    tensor = np.ones((sorted_anns[0]['segmentation'].shape[0], sorted_anns[0]['segmentation'].shape[1], 1))

    # 遍历每个注释，并将其对应的掩码区域用随机颜色填充到图像数组中
    ii = 0
    ll = len(sorted_anns)
    for ann in sorted_anns:
        ii += 1
        m = ann['segmentation']
        tensor[m] = ii
        if ii > ll // 2:
            break

    return tensor


def create_masks(image):
    sam = sam_model_registry["default"](checkpoint=ct.SAM_MODEL_PATH)
    mask_generator = SamAutomaticMaskGenerator(sam)
    masks = mask_generator.generate(image)
    return masks


def create_tensor(image):
    masks = create_masks(image)
    tensor = show_anns(masks)
    return tensor


class SAMwrapper(object):
    def __init__(self, mtype, mpath):
        self.model_type_ = mtype
        self.sam_ = sam_model_registry[mtype](checkpoint=mpath)
        self.device_ = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.sam_.to(device=self.device_)
        self.predictor_ = SamPredictor(self.sam_)

    def predict_mask(self, image, prompt_pts):
        self.predictor_.set_image(image)
        input_point = np.array(prompt_pts)
        input_label = np.array([1 for _ in range(len(prompt_pts))]) # 每个点都是同一个标签
        masks, scores, logits = self.predictor_.predict(
            point_coords=input_point,
            point_labels=input_label,
            multimask_output=True,
        )
        return masks, scores, logits


