# -*- coding: UTF-8 -*-
from PIL import Image
import os
import path


def rotation(angle, g):
    img = Image.open(g['src'] + g['name'] + g['form'])
    img_rotate = img.rotate(angle, expand=True)
    # img_rotate.show()
    img_rotate.save(g['dst'] + g['name'] + g['form'])


def transpose(g, pos):
    img = Image.open(g['src'] + g['name'] + g['form'])
    img_transpose = img.transpose(pos)
    # img_transpose.show()
    img_transpose.save(g['dst'] + g['name'] + g['form'])


def process(group):
    if group['num'] == 1:
        rotation(90, group)
    if group['num'] == 2:
        rotation(180, group)
    if group['num'] == 3:
        rotation(270, group)
    if group['num'] == 4:
        transpose(group, Image.FLIP_TOP_BOTTOM)
    if group['num'] == 5:
        transpose(group, Image.FLIP_LEFT_RIGHT)


def main():
    a = 1
    b = 1
    json = '_json/'
    for a in range(1, 301):
        src = path.src + str(a) + json
        for b in range(1, 6):
            # print(5*a+b+295)
            dst = path.dst + str(5*a+b+295) + json
            print(dst)
            os.chdir(src)
            for i in os.listdir(os.getcwd()):
                # 检查前缀
                if os.path.splitext(i)[0] == 'img':
                    group = {'src':  src,
                             'dst':  dst,
                             'name': os.path.splitext(i)[0],
                             'form': os.path.splitext(i)[1],
                             'num':  b}
                    process(group)

                if os.path.splitext(i)[0] == 'label':
                    group = {'src':  src,
                             'dst':  dst,
                             'name': os.path.splitext(i)[0],
                             'form': os.path.splitext(i)[1],
                             'num':  b}
                    process(group)


if __name__ == '__main__':
    main()
