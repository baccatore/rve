#!/usr/bin/env python3
#coding:utf8
#cython:language_level=3, boundscheck=False
import time
from libcpp.vector cimport vector
import itertools
import numpy as np
cimport numpy as np
cimport cython

def count(vector[vector[short]] xyz,
        vector[unsigned short]  candidate_range,
        vector[unsigned short]  candidate_size,
        short progress_plot_rate = 10000):
    cdef int i, j, k
    cdef unsigned int total_xyz, current_xyz, ijk
    cdef vector[unsigned short] cell_xyz = [0]*3
    cdef vector[short] trgt_grd_rng = [0]*3*2
    cdef vector[long] nb_cell_in_candidate_ijk = [0]*np.prod(candidate_range)

    total_xyz = len(xyz)
    t1 = time.clock()
    for current_xyz, cell_xyz in enumerate(xyz):
        if current_xyz%progress_plot_rate == 0:
            t2 = time.clock()
            print('Counting... {0:>10}/{1} cells, '
                    '{2: 3.1f}%, {3: 3.1f} sec per {4:,} loops'
                    .format(current_xyz,total_xyz,current_xyz/total_xyz*100,
                    t2-t1,progress_plot_rate))
            t1 = t2

        for i in range(3):
            trgt_grd_rng[i]   = cell_xyz[i] - candidate_size[i]
            trgt_grd_rng[i+3] = cell_xyz[i]
            if trgt_grd_rng[i] < 0:
                trgt_grd_rng[i]   = 0
            elif  trgt_grd_rng[i+3] > candidate_range[i]:
                trgt_grd_rng[i+3] = candidate_range[i]

        for i, j, k in itertools.product(
                range(trgt_grd_rng[0], trgt_grd_rng[3]),
                range(trgt_grd_rng[1], trgt_grd_rng[4]),
                range(trgt_grd_rng[2], trgt_grd_rng[5])):
            ijk= i+j*candidate_range[0]+k*candidate_range[0]*candidate_range[1]
            nb_cell_in_candidate_ijk[ijk] += 1
        
    print('\n')
    return nb_cell_in_candidate_ijk
