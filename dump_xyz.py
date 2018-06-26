#!/usr/bin/env python3
#coding:utf8
#************************dump_xyz.py*************************
# Author    : Yuichiro SUGA
# Email     : yuichiro.suga@centraliens-lille.org
# Created   : 2018-06-22 PM 02:59:18
# Modified  : 2018-06-22 PM 02:59:18
# Binarize a .xyz file in text
#************************************************************

import pickle
import sys

text_file, binary_file = sys.argv[1], sys.argv[2]
data = ''

def bump_txt2xyz(text_file, binary_file):
    with open(text_file,'r') as tf:
        data = tf.read()

    with open(binary_file,'wb') as bf:
        pickle.dump(data,bf)


if __name__ == "__main__":
    bump_txt2xyz(text_file, binary_file)
    print('\033[32mDumped',text_file, 'into', binary_file, '\033[m')
