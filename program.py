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
                    xyz.append((i+1,j+1,k+1))
    return xyz


def load_images(address):
    xyz = []
    file_list = glob.glob(address)
    nb_file = len(file_list)
    file_list.sort()
    for i, file_name in enumerate(file_list):
        xyz += read_pbm(file_name)
        print('\rReading...', file_name, i+1, '/', nb_file, flush=True, end='')
    return xyz

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


@jit
def count_cells(xyz, candidate_range, candidate_size):
    t1 = start
    nb_cell_in_candidate_ijk = np.ndarray(candidate_range)
    total = len(xyz)
    trgt_grd_rng = np.zeros(6, dtype=np.int).reshape((3,2))
    for current, cell_xyz in enumerate(map(np.array,xyz)):
        #target grid zone
        trgt_grd = cell_xyz - candidate_size
        
        #approximately 500 msec per cell
        #for i in range(3):
            #TODO revise following 3 lines
        #    trgt_grd_rng[i][0] = trgt_grd[i]
        #    trgt_grd_rng[i][1] = cell_xyz[i]
        #    if trgt_grd_rng[i][0] < 0:
        #        trgt_grd_rng[i][0] = 0
        #    if trgt_grd_rng[i][1] > candidate_range[i]:
        #        trgt_grd_rng[i][1] = candidate_range[i]

        #for k in range(trgt_grd_rng[2][0], trgt_grd_rng[2][1]):
        #    for j in range(trgt_grd_rng[1][0], trgt_grd_rng[1][1]):
        #        for i in range(trgt_grd_rng[0][0], trgt_grd_rng[0][1]):
        #for i,j,k in itertools.product( \
        #        range(trgt_grd_rng[0][0], trgt_grd_rng[0][1]), \
        #        range(trgt_grd_rng[1][0], trgt_grd_rng[1][1]), \
        #        range(trgt_grd_rng[2][0], trgt_grd_rng[2][1])):
        #            nb_cell_in_candidate_ijk[i][j][k] +=1

        for i,j,k in itertools.product( \
                range(candidate_range[0]), \
                range(candidate_range[1]), \
                range(candidate_range[2])):
            xi = np.array([i,j,k],dtype=np.int)
            a = xi - (cell_xyz + 1)
            b = xi + cell_xyz + 1 - candidate_size
            flag = 0
            for elem in a*b:
                if elem < 0:
                    flag +=1
            if flag == 3:
               nb_cell_in_candidate_ijk += 1

        if current%1 == 0:
            t2 = time.time()
            lap = t2 - t1
            t1 = t2
            print('\r{0}/{1} Runtime: {2:.3f}     '.format(current,total,lap),flush=True,end='')
    return nb_cell_in_candidate_ijk

if __name__ == '__main__':
    #Prologue: Run timer
    start = time.time()

    #Main routine
    xyz = load_images('./eguchi_hangetsuban_ascii/*.pbm')
    write_xyz('result.xyz', xyz, binary=True)
    #TODO Read automatically from image data
    print('Loading...')
    with open('result_binary_list.xyz','rb') as f:
        xyz = pickle.load(f)
    print('Counting...')
    population_size   = np.array((1024, 1024, 130),dtype=np.int)
    population_volume = np.prod(population_size)
    candidate_size    = np.array((128,   128,  32),dtype=np.int)
    candidate_range   = population_size - candidate_size + 1
    candidate_nb      = np.prod(candidate_range)
    candidate_volume  = np.prod(candidate_size)
    #result = count_cells(xyz, candidate_range, candidate_size)
    with open('count_result','rb') as f:
        pickle.dump(result,f)

    #FIXME Make me easier!
    #Epilogue
    end = time.time() - start
    print('\033[32mEnd of program: Run time {0:.3f} sec\033[m'.format(end))
