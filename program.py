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
import glob
import re
import pickle
import time
import itertools

import numpy as np
from numba import jit

import cell_count

def read_pbm(file_name):
    xyz = []
    result = re.search(r'\d+\.pbm$', file_name)
    result = re.search(r'[0-9]+', result.group(0))
    if result:
        k = int(result.group(0))

    with open(file_name,'r') as f:
        if f.readline()[0:2] != 'P1':
            #TODO raise error
            print('\033[31mOnly P1 type pbm file is acceptable\033[m')
            return
        
        for line in f:
            if line[0] == '#':
                continue
            x_max, y_max = tuple(map(int,line.split()))
            break

        for j, line in enumerate(f):
            #Array of cells in line y_i
            yi = line.split()
            f.readline()
            for i, xiyj in enumerate(yi):
                #Input is as string
                if xiyj == '1':
                    #Coordinate starts from 0
                    xyz.append([i+1,j+1,k+1])
    return xyz


@jit
def load_images(address):
    xyz = []
    file_list = glob.glob(address)
    nb_file = len(file_list)
    file_list.sort()
    for i, file_name in enumerate(file_list):
        xyz += read_pbm(file_name)
        print('\rReading...', file_name, i+1, '/', nb_file, flush=True, end='')
    return xyz


@jit
def write_xyz(file_name, xyz, binary=False):
    print('\nWriting output...')
    with open('result.xyz','w') as f:
        for line in xyz:
            coordinate = " ".join(map(str,line))
            f.write(coordinate + "\n")
    if binary:
        print('Writing output in binary...')
        with open('result_binary.xyz','wb') as f:
           pickle.dump(xyz,f)


if __name__ == '__main__':
    #Prologue: Run timer
    start = time.clock()

    #Main routine
    #xyz = load_images('./eguchi_hangetsuban_ascii/*.pbm')
    #write_xyz('result.xyz', xyz)
    #TODO Read automatically from image data
    with open('result_binary.xyz','rb') as f:
        xyz = pickle.load(f)
    
    population_size   = np.array((1024, 1024, 130))
    #population_volume = np.prod(population_size)
    candidate_size    = np.array((128,   128,  32))
    candidate_range   = population_size - candidate_size + 1
    #candidate_nb      = np.prod(candidate_range)
    #candidate_volume  = np.prod(candidate_size)
    result = cell_count.count(xyz, candidate_range, candidate_size)
    with open('count_result','wb') as f:
        pickle.dump(result,f)

    #FIXME Make me easier!
    #Epilogue
    end = time.clock() - start
    print('\033[32mEnd of program: Run time {0:.3f} sec\033[m'.format(end))
