import re
import pickle
import glob
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
                if xiyj == '0':
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
    print('\n')
    return xyz


def write_xyz(file_name, xyz, binary=False):
    print('\nWriting output...')
    with open(file_name,'w') as f:
        for line in xyz:
            coordinate = " ".join(map(str,line))
            f.write(coordinate + "\n")
    if binary:
        print('Writing output in binary...')
        with open('binary_'+file_name,'wb') as f:
           pickle.dump(xyz,f)
