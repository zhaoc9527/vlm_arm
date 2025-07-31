import math

import cv2
import numpy as np


def map_image_to_robot(x,y):
   # 标定点 - 图像坐标（像素）
    pts_img = np.float32([
        [231, 549],     # 点 A
        [737, 181],     # 点 B
        [548, 477],     # 点 C
    ])

    # 标定点 - 机械臂坐标（单位：米）
    pts_arm = np.float32([
        [235.882 / 1000.0, 169.301 / 1000.0],   # A
        [347.501 / 1000.0, -5.745 / 1000.0],   # B
        [251.961  / 1000.0, 42.57   / 1000.0],   # C
    ])

    # 计算仿射变换矩阵（2x3）
    M = cv2.getAffineTransform(pts_img, pts_arm)

    # 输入点
    input_point = np.array([[x, y]], dtype=np.float32)  # shape: (1, 2)
    input_point = np.expand_dims(input_point, axis=0)   # shape: (1, 1, 2)

    # 应用仿射变换
    transformed = cv2.transform(input_point, M)
    X, Y = transformed[0][0]
    return X, Y

if __name__ == '__main__':
    x,y = map_image_to_robot(548, 477)
    print(x,y)