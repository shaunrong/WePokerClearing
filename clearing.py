#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals

import argparse

import re
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

    for

    print("STEP 1: Apply OCR to extract strings from the receipt")
    receipt_str = pytesseract.image_to_string(Image.open(args.i))
    print(receipt_str)
    print("STEP 2: Extract all float numbers through regex matching")
    num_str_on_receipt = re.findall("\d+\.\d+", receipt_str)
    num_on_receipt = [float(s) for s in num_str_on_receipt]
    print(num_on_receipt)
    print("STEP 3: Conclusion")
    print("Your spending on this transaction is {} USD".format(max(num_on_receipt)))