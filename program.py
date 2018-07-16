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


use_binary_file = False 

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
        print('Reading image files...')
        xyz, population_size = util.load_images('./input_images/*.pbm')
        util.write_xyz('input.xyz', (xyz, population_size), binary=False)


    seed = np.array([1,1,1])
    for i in range(128,129):
        candidate_size    = seed*i
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
                population_size,
                candidate_range,
                candidate_size,
                progress_plot_rate = 10000)
        print('Writing result in count_result...')
        with open('count_result_{0:03d}'.format(i),'w') as f:
            f.writelines([ str(val)+'\n'  for val in result ])
        print(datetime.datetime.now())
        print('-----------------')

    #Epilogue
    end = time.time() - start
    print('\033[32mEnd of program: Run time {0:.3f} sec\033[m'.format(end))
