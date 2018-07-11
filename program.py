#!/usr/bin/env python3
#coding:utf8
#*************************pbm2xyz.py*************************
# Author    : Yuichiro SUGA
# Email     : yuichiro.suga@centraliens-lille.org
# Created   : 2018-06-22 PM 02:37:01
# Modified  : 2018-06-22 PM 02:37:01
# Convert a set of pbm files into a .xyz file
#************************************************************

import sys
import time
import datetime
import pickle

import numpy as np
from joblib import Parallel, delayed

import cell_count
import util


if __name__ == '__main__':
    #Prologue: Run timer
    start = time.time()
    print("Program prologue...")

    #Main routine
    xyz = util.load_images('./input_images/*.pbm')
    util.write_xyz('binary_input.xyz', xyz, binary=True)

    #print("Opening result_binary.xyz")
    #with open('binary_input.xyz','rb') as f:
    #    xyz = pickle.load(f)
    population_size   = np.ones(3)*1024
    population_volume = np.prod(population_size)
    print('Population size', population_size)
    print('Population volume', population_volume)

    seed = np.array({32,32,8})
    print('-----------------')
    print('Counting:', seed)
    print(datetime.datetime.now())
    candidate_size    = seed
    candidate_range   = population_size - candidate_size + 1
    candidate_nb      = np.prod(candidate_range)
    candidate_volume  = np.prod(candidate_size)
    result = cell_count.count(
            xyz,
            candidate_range,
            candidate_size,
            progress_plot_rate=10000)

    print('\nWriting result in count_result...')
    with open('count_result_'+str(seed),'w') as f:
        f.writelines([ str(val)+'\n'  for val in result ])
    print(datetime.datetime.now())

    #Epilogue
    end = time.time() - start
    print('\033[32mEnd of program: Run time {0:.3f} sec\033[m'.format(end))
