import numpy as np
import glob
import pickle
from statistics import mean
from matplotlib import pyplot as plt

def calc_rss(raw_data, candidate_range, candidate_size, phi_avg):
    # vc: candidate volume
    # i : index for candidate position in population
    vc_total_rcp = 1. / np.prod(candidate_size)

    phi_i = [ vc_cell_i * vc_total_rcp for vc_cell_i in raw_data ]
    if any([phi > 1 for phi in phi_i]):
        raise ValueError('phi must be smaller than 1.0')
    residual_square  = lambda phi : (phi - phi_avg)**2
    residual_squares = map(residual_square, phi_i)

    return sum(residual_squares) / np.prod(candidate_range)

if __name__ == '__main__':
    rss_i = []
   # population_size = [128]*3
   # phi_avg = 129704 / np.prod(population_size)
   # print('phi_avg', phi_avg)
   # file_list = glob.glob('./output_cell_count/count_result_*')
   # file_list.sort()
   # for i, file_name in enumerate(file_list,1):
   #     print('Analysing... ' + file_name)
   #     with open(file_name, 'r') as f:
   #         raw_data = map(int,f.readlines())
   #     del f
   #     candidate_size  = np.array([i]*3)
   #     candidate_range = population_size - candidate_size + 1
   #     rss_i.append(calc_rss(raw_data,
   #         candidate_range, candidate_size, phi_avg))

   # with open('rss_curve.txt', 'wb') as f:
   #     pickle.dump(rss_i,f)

    with open('rss_curve.txt', 'rb') as f:
        rss_i = pickle.load(f)
    print(rss_i)

    x_vec = [i for i in range(1,129)]
    y_vec = []
    y1 = y2 = .0
    for y in rss_i:
        y_vec.append(y1-y2)
        y1, y2 = y2, y
    plt.semilogy()
    plt.plot(x_vec, y_vec)
    plt.plot(x_vec, rss_i)
    plt.plot([1,128], [.000001,.000001], color='black',linestyle='dashed', linewidth=.5)
    plt.plot([1,128], [.00001,.00001], color='black',linestyle='dashed', linewidth=.5)
    plt.plot([1,128], [.0001,.0001], color='black',linestyle='dashed', linewidth=.5)
    plt.plot([1,128], [.001,.001], color='black',linestyle='dashed', linewidth=.5)
    plt.savefig('image_def.png')
    plt.show()
