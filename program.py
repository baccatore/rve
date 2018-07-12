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
#from joblib import Parallel, delayed

import cell_count
import util


use_binary_file = True

if __name__ == '__main__':
    #Prologue: Run timer
    start = time.time()
    print("Program prologue...")

    #Main routine
    if use_binary_file:
        print("Opening result_binary.xyz")
        with open('binary_input.xyz','rb') as f:
            xyz, population_size = pickle.load(f)
    else:
        xyz, population_size = util.load_images('./input_images/*.pbm')
        util.write_xyz('input.xyz', (xyz, population_size), binary=True)


    seed = np.array([32,32,8])
    candidate_size    = seed
    candidate_range   = population_size - candidate_size + 1
    candidate_nb      = np.prod(candidate_range)
    candidate_volume  = np.prod(candidate_size)
    print('-----------------')
    print('Start time      :',
            datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    print('Population size :', population_size)
    print('Candidate size  :', candidate_size)
    print('Candidate range :', candidate_range)
    print('Candidate number:', candidate_nb)
    print('Candidate volume:', candidate_volume)
    print('Count starts')
    result = cell_count.count(
            xyz,
            candidate_range,
            candidate_size)
    print('-----------------')

    print('Writing result in count_result...')
    with open('count_result_'+str(seed),'w') as f:
        f.writelines([ str(val)+'\n'  for val in result ])
    print(datetime.datetime.now())

    #Epilogue
    end = time.time() - start
    print('\033[32mEnd of program: Run time {0:.3f} sec\033[m'.format(end))
