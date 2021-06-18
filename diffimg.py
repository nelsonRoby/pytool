#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Pastes another image into this image.
    The box argument is either a 2-tuple giving the upper left corner, a 4-tuple defining the left, upper,
    right, and lower pixel coordinate, or None (same as (0, 0)). If a 4-tuple is given, the size of the pasted
    image must match the size of the region.
"""

from PIL import Image
from PIL import ImageChops
def compare_images(path_one, path_two, diff_save_location):
    """
    比较图片，如果有不同则生成展示不同的图片
    @参数一: path_one: 第一张图片的路径
    @参数二: path_two: 第二张图片的路径
    @参数三: diff_save_location: 不同图的保存路径
    """
    image_one = Image.open(path_one)
    image_two = Image.open(path_two)
    try:
        diff = ImageChops.difference(image_one, image_two)
        if diff.getbbox() is None:
            print("We are the same!")
        else:
            diff.save(diff_save_location)
    except ValueError as e:
        print("{}".format(e))

if __name__ == '__main__':
    compare_images('1.png','2.png','diff.png')
