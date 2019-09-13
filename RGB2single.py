# coding:utf-8

import numpy as np
import cv2
import os
from PIL import Image

# 源目录
MyPath = 'C:/Users/12084/Desktop/Proj/data/9-8/test/'
# 输出目录
OutPath = 'C:/Users/12084/Desktop/Proj/data/9-8/test/G/'


def process(src, dst, name):
    """
    src是存放待转换图片的目录
    dst是存在输出转换后图片的目录
    name是文件名
    """
    # 打开图片
    img = cv2.imread(src + name)
    # 提取G通道
    b, g, r = cv2.split(img)
    # 创建与image相同大小的零矩阵
    zeros = np.zeros(img.shape[:2], dtype="uint8")
    cv2.imwrite(dst + name, cv2.merge([zeros, g, zeros]))  # [R, G, B]


def run():
    # 切换到源目录，遍历源目录下所有图片
    os.chdir(MyPath)
    for i in os.listdir(os.getcwd()):
        # 检查后缀
        postfix = os.path.splitext(i)[1]
        if postfix == '.jpg':
            process(MyPath, OutPath, i)


if __name__ == '__main__':
    run()
