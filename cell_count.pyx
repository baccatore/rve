#!/usr/bin/env python3
#coding:utf8
#cython:language_level=3, boundscheck=False
import time
from libcpp.vector cimport vector
import itertools
import numpy as np
cimport numpy as np
cimport cython


DTYPE = np.int
ctypedef np.int_t DTYPE_t

cdef print_progress(t1, current_xyz, total_xyz, progress_plot_rate):
    t2 = time.clock()
    print('Counting... {0:>10}/{1} cells, '
            '{2: 3.1f}%, {3: 3.1f} sec per {4:,} loops'
            .format(current_xyz,total_xyz,current_xyz/total_xyz*100,
            t2-t1,progress_plot_rate))
    return t2


cdef focus_method(vector[vector[int]] xyz,
        vector[int]  candidate_range,
        vector[int]  candidate_size,
        int progress_plot_rate):
    cdef int i, j, k
    cdef int current_xyz, total_xyz, ijk
    cdef vector[int] cell_xyz  = [0]*3
    cdef vector[long] nb_cell_in_candidate_ijk = [0]*np.prod(candidate_range)
    cdef vector[int] start_end = [0]*3
    cdef vector[int] stop_end  = [0]*3

    total_xyz = len(xyz)
    t = time.clock()
    for current_xyz, cell_xyz in enumerate(xyz):
        if current_xyz%progress_plot_rate == 0:
            t = print_progress(t, current_xyz, total_xyz, progress_plot_rate)

        for i in range(3):
            start_end[i] = cell_xyz[i] - candidate_size[i] + 1
            if start_end[i] < 0:
                start_end[i] = 0

            stop_end[i] = cell_xyz[i] + 1
            if stop_end[i] > candidate_range[i]:
                stop_end[i]  = candidate_range[i]

        for i, j, k in itertools.product(
                range(start_end[0], stop_end[0]),
                range(start_end[1], stop_end[1]),
                range(start_end[2], stop_end[2])):
            ijk= i+j*candidate_range[0]+k*candidate_range[0]*candidate_range[1]
            nb_cell_in_candidate_ijk[ijk] += 1
        
    return nb_cell_in_candidate_ijk


cdef sweep_method(vector[vector[short]] xyz,
        np.ndarray  candidate_range,
        vector[int]  candidate_size,
        int progress_plot_rate):
    cdef int i, j, k
    cdef int current_xyz, total_xyz, ijk
    cdef vector[int] cell_xyz = [0]*3 
    cdef vector[long] nb_cell_in_candidate_ijk = \
            [0]*np.prod(candidate_range)
    cdef np.ndarray candidate_xyz = np.zeros(3, dtype=DTYPE)
    cdef np.ndarray a = np.zeros(3, dtype=DTYPE)
    cdef np.ndarray b = np.zeros(3, dtype=DTYPE)

    total_xyz = len(xyz)
    t = time.clock()
    for current_xyz, cell_xyz in enumerate(xyz):
        if current_xyz%progress_plot_rate == 0:
            t = print_progress(t, current_xyz, total_xyz, progress_plot_rate)

        for i, j, k in itertools.product(
                range(candidate_range[0]),
                range(candidate_range[1]),
                range(candidate_range[2])):
            ijk= i+j*candidate_range[0]+k*candidate_range[0]*candidate_range[1]
            candidate_xyz = np.array([i, j, k])
            
            #In order to write following three lines 'flatly'
            # numpy is mixed with cython.vector here... 
            a =  candidate_xyz - cell_xyz
            b = (candidate_xyz + candidate_size - 1) - cell_xyz

            if all(a*b <= 0):
                nb_cell_in_candidate_ijk[ijk] += 1

    return nb_cell_in_candidate_ijk


def count(xyz, population_size, candidate_range, candidate_size,
        progress_plot_rate = 10000):
    #if candidate_size[0]/population_size[0] > 0.5:
    if True:
        print('Method: Focus method')
        return focus_method(xyz, candidate_range,
                candidate_size, progress_plot_rate)
    else :
        print('Method: Sweep method')
        return sweep_method(xyz, candidate_range,
                candidate_size, progress_plot_rate)

