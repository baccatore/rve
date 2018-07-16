import numpy as np
import glob
from matplotlib import pyplot as plt

def calc_rss(raw_data, candidate_size, phi_avg):
    # vc: candidate volume
    # i : index for candidate position in population
    vc_total = np.prod(candidate_size)

    phi_i = [ vc_cell_i / vc_total for vc_cell_i in raw_data ]
    residual_square  = lambda phi : (phi - phi_avg)**2
    residual_squares = map(residual_square, phi_i)
    
    return sum(residual_squares)

if __name__ == '__main__':
    rss_i = []
    phi_avg = 0.0614

    file_list = glob.glob('./output_cell_count/count_result_*')
    file_list.sort()
    print([0]*3)
    for i, file_name in enumerate(file_list):
        print('Analysing... ' + file_name)
        with open(file_name, 'r') as f:
            raw_data = map(int,f.readlines())
        del f
        rss_i.append(calc_rss(raw_data, [i+1]*3, phi_avg))

    plt.semilogy([i for i in range(1,128)], rss_i)
    plt.plot([1,128], [.00001,.00001], color='black',linestyle='dashed', linewidth=.5)
    plt.show()
