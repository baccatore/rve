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
            raise ValueError('\033[31mOnly P1 type pbm file is acceptable\033[m')
            return
        
        for line in f:
            if line[0] == '#':
                continue
            x_max, y_max = tuple(map(int,line.split()))
            break

        for j, line in enumerate(f):
            #Take line number as y
            yi = line.split()
            f.readline()
            for i, pixel_value in enumerate(yi):
                #Input is as string
                if pixel_value == '0':
                    xyz.append((i,j,k))
    return (xyz, x_max, y_max)


def load_images(address):
    xyz   = []
    xyz_i = []
    x_max = y_max = 0
    file_list = glob.glob(address)
    nb_file = len(file_list)
    file_list.sort()
    for i, file_name in enumerate(file_list):
        xyz_i, x_max, y_max = read_pbm(file_name)
        xyz += xyz_i
        print('\rReading... {0} {1:>3}/{2:<3}'.format(file_name, i+1, nb_file), flush=True, end='')
    print('\n', x_max, y_max)
    return (np.array([ [x,y,z] for x, y, z in xyz ]), np.array((x_max, y_max, nb_file) ))


def write_xyz(file_name, data, binary=False):
    print('Writing ' + file_name + '...')
    if binary:
        with open('binary_'+file_name,'wb') as f:
           pickle.dump(data,f)
    else :
        xyz, population_size = data
        with open(file_name,'w') as f:
            f.write('{0[0]} {0[1]} {0[2]}\n'.format(population_size))
            for line in xyz:
                f.write('{0[0]} {0[1]} {0[2]}\n'.format(line))

