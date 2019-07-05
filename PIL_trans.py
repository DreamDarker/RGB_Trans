# coding:utf-8
import os
from PIL import Image
# 源目录
MyPath = 'C:/Users/12084/Desktop/Proj/data/test/mask/'
# 输出目录
OutPath = 'C:/Users/12084/Desktop/Proj/data/test/mask8/'

def processImage(filesoure, destsoure, name, imgtype):
    '''
    filesoure是存放待转换图片的目录
    destsoure是存在输出转换后图片的目录
    name是文件名
    imgtype是文件类型
    '''
    imgtype = 'png'

    # 打开图片
    im = Image.open(filesoure + name)
    # 操作转8bit
    width = im.size[0]
    height = im.size[1]

    for x in range(width):
      for y in range(height):
        if(im.getpixel((x, y))>0):
           im.putpixel((x, y), 1)
        else:
            im.putpixel((x, y), 0)
    im.save(destsoure + name, imgtype)


def run():
    # 切换到源目录，遍历源目录下所有图片
    os.chdir(MyPath)
    for i in os.listdir(os.getcwd()):
        #检查后缀
        postfix = os.path.splitext(i)[1]
        if  postfix == '.png':
            processImage(MyPath, OutPath, i, postfix)


if __name__ == '__main__':
    run()