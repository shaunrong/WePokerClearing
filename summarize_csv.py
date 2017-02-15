#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __future__ import unicode_literals

import os
from collections import defaultdict

import yaml
import csv

__author__ = 'Ziqin (Shaun) Rong'
__maintainer__ = 'Ziqin (Shaun) Rong'
__email__ = 'rongzq08@gmail.com'


if __name__ == '__main__':
    sum_book = defaultdict(lambda: 0)
    sum_book_dict = {}
    for f in os.listdir('tmp'):
        if f.split('.')[-1] == 'yaml':
            tmp_game_book = yaml.load(open(os.path.join('tmp', f), 'rb'))
            game_book = {}
            for k, v in tmp_game_book.items():
                game_book[k.encode('utf-8')] = v
            sum_book_dict[f[:-5].encode('utf-8')] = game_book

    for game, book in sum_book_dict.items():
        for player, pnl in book.items():
            sum_book[player] += pnl

    with open('summary.csv', 'w') as csv_f:
        writer = csv.writer(csv_f)
        header = ["players"] + sum_book_dict.keys() + ['summary']
        players = sum_book.keys()
        writer.writerow(header)
        for p in players:
            new_row = [p]
            for i, game in enumerate(header):
                if i != 0 and i != len(header) - 1:
                    if p in sum_book_dict[game].keys():
                        new_row += [sum_book_dict[game][p]]
                    else:
                        new_row += [0]
                if i == len(header) - 1:
                    new_row += [sum_book[p]]
            writer.writerow(new_row)
