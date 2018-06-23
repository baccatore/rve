#!/usr/bin/env python3
#coding:utf8
#cython: language_level=3, boundscheck=False
import time
from libcpp.vector cimport vector
cimport cython

def count(vector[:,:] xyz, \
        vector[unsigned short] candidate_range, \
        vector[unsigned short] candidate_size):
    cdef float t1, t2
    cdef unsigned short i, j, k
    cdef unsigned int total_xyz, current_xyz, ijk
    cdef vector[unsigned long] nb_cell_in_candidate_ijk
    cdef vector[unsigned short]cell_xyz
    cdef vector[unsigned short] trgt_grd
    cdef vector[unsigned short] trgt_grd_rng

    t1 = time.time()
    total_xyz = len(xyz)
    for current_xyz, cell_xyz in enumerate(xyz):
        #target grid zone
        for i in range(3):
            trgt_grd[i] = cell_xyz[i] - candidate_size[i]
        for i in range(3):
            for j in range(2):
                trgt_grd_rng[i+j*3] = 0
        
        for i in range(3):
            #TODO revise following 3 lines
            if trgt_grd_rng[i] < 0:
                trgt_grd_rng[i] = 0
                trgt_grd_rng[i+3] = cell_xyz[i]
            elif trgt_grd_rng[i+3] > candidate_range[i]:
                trgt_grd_rng[i] = trgt_grd[i]
                trgt_grd_rng[i+3] = candidate_range[i]
            else:
                trgt_grd_rng[i] = trgt_grd[i]
                trgt_grd_rng[i+3] = cell_xyz[i]

        for i in range(trgt_grd_rng[0], trgt_grd_rng[3]):
            for j in range(trgt_grd_rng[1], trgt_grd_rng[4]):
                for k in range(trgt_grd_rng[2], trgt_grd_rng[5]):
                    ijk = i + j*candidate_range[0] + k*candidate_range[0]*candidate_range[1]
                    nb_cell_in_candidate_ijk[ijk] +=1


        if current_xyz%100 == 0:
            t2 = time.time()
            print('\r{0}/{1} Runtime: {2:.3f}     '.format(current_xyz,total_xyz, t2-t1),flush=True,end='')
            t1 = t2
    return nb_cell_in_candidate_ijk
