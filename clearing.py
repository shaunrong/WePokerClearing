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
import yaml

from collections import defaultdict

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
            # print(clearing_str)
            str_l = clearing_str.splitlines()

            game_book = {}
            zero_l_num = None
            for l_num, line in enumerate(str_l):
                line = line.decode('utf-8')
                line_l = line.split()
                if "买入" in line_l:
                    player = " ".join(line_l[:line_l.index("买入")]).encode("utf-8")
                    pnl = "".join(line_l[line_l.index("买入") + 2:]).encode("utf-8")
                    # print(pnl)
                    if pnl == "0" or pnl == 'O' or pnl == 'o':
                        pnl = 0
                        zero_l_num = l_num
                    elif pnl[0] == "+":
                        pnl = int(pnl[1:])
                    elif pnl[0] == "-" or pnl[0] == "_":
                        pnl = -1 * int(pnl[1:])
                    elif l_num > zero_l_num:
                        pnl = -1 * int(pnl[1:])

                    if not player:
                        print("missing a player on line {} at pnl {}".format(l_num, pnl))
                        game_book['missing_player'.encode('utf-8')] = pnl
                    else:
                        game_book[player] = pnl

            yaml_f_name = "_".join(f.split('.')[:-1]) + ".yaml"
            with open(os.path.join('tmp', yaml_f_name), 'wb') as yf:
                yaml.safe_dump(game_book, yf, default_flow_style=False, allow_unicode=True)

