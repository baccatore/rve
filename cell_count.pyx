#!/usr/bin/env python3
#coding:utf8
#cython: language_level=3, boundscheck=False
import time
import itertools
from libcpp.vector cimport vector
cimport cython

def count(vector[vector[short]] xyz, \
        vector[unsigned short]  candidate_range, \
        vector[unsigned short]  candidate_size):
    cdef float t1, t2
    cdef int   i, j, k
    cdef unsigned int total_xyz, current_xyz, ijk
    cdef vector[unsigned long]  nb_cell_in_candidate_ijk
    cdef vector[unsigned short] cell_xyz
    cdef vector[short] trgt_grd_rng

    t1 = time.clock()
    total_xyz = len(xyz)
    for current_xyz, cell_xyz in enumerate(xyz):
        for i in range(3):
            trgt_grd_rng[i]   = cell_xyz[i] - candidate_size[i]
            trgt_grd_rng[i+3] = cell_xyz[i]
            if trgt_grd_rng[i] < 0:
                trgt_grd_rng[i] = 0
            elif trgt_grd_rng[i+3] > candidate_range[i]:
                trgt_grd_rng[i+3] = candidate_range[i]

        for i, j, k in itertools.product(
                range(trgt_grd_rng[0], trgt_grd_rng[3]),
                range(trgt_grd_rng[1], trgt_grd_rng[4]),
                range(trgt_grd_rng[2], trgt_grd_rng[5])):
            ijk = i + j*candidate_range[0] + k*candidate_range[0]*candidate_range[1]
            nb_cell_in_candidate_ijk[ijk] +=1


        if current_xyz%100 == 0:
            t2 = time.clock()
            print('\r{0}/{1} Runtime: {2:.3f}     '.format(current_xyz,total_xyz, t2-t1),flush=True,end='')
            t1 = t2
    return nb_cell_in_candidate_ijk
