#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals

import argparse
import os
import cv2
import numpy as np
import shutil

from PIL import Image
from pytesseract import pytesseract

__author__ = 'Ziqin (Shaun) Rong'
__version__ = '0.1'
__maintainer__ = 'Ziqin (Shaun) Rong'
__email__ = 'rongzq08@gmail.com'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required=True, help="Path to the file where the clearing pictures are stored")
    args = parser.parse_args()

    if os.path.exists('tmp'):
        shutil.rmtree("tmp")
    os.mkdir('tmp')

    for f in os.listdir(args.i):
        if f.split('.')[-1] == 'jpeg':
            img = cv2.imread(os.path.join(args.i, f))
            b = img[:, :, 0]
            g = img[:, :, 1]
            r = img[:, :, 2]
            height, width = r.shape
            processed_img = np.ones((height, width)) * 255
            for i in range(height):
                for j in range(width):
                    if r[i, j] == g[i, j] == b[i, j] and r[i, j] < 230:
                        img[i, j, :] = 0
            cv2.imwrite(os.path.join("tmp", f), img)

            print("processing file {}".format(f))
            img = Image.open(os.path.join('tmp', f))
            clearing_str = pytesseract.image_to_string(img, lang='chi_sim')
            print(clearing_str)