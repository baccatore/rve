
import pickle
xyz = []

with open('eguchi_hangetsuban_ascii/hangetsu_0607_100.pbm', 'r') as f:
    if f.readline()[0:2] != 'P1':
        raise Exception('\033[31mOnly P1 type pbm file is acceptable\033[m')

    for line in f:
        if line[0] == '#':
            continue
        x_max, y_max = tuple(map(int,line.split()))
        break

    for line in f:
        yi = line.split()
        f.readline()
        for xiyj in yi:
            assert xiyj != 0 or xiyj !=1, 'Something worng in original data'
            if xiyj == '1':
                xyz.append(True)
            else :
                xyz.append(False)

with open('test_pbm_bitnize', 'wb') as f:
    pickle.dump(xyz, f)
 
for i in xyz:
    print(bin(i))
