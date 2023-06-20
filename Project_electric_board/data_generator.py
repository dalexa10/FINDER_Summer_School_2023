import random
import os
import pickle
import numpy
import numpy as np
import math
import pandas as pd

from circuit_model import is_device_safe, is_component_inside, is_capacitor_safe, is_thermal_cycling_safe

# These are the parameters of the board that you can control as inputs to the function
def monte_carlo_board(n_points, nround=1):
    board_cases = []
    for _ in range(n_points):
        L = round(random.uniform(0.5, 5.), nround)
        H = round(random.uniform(0.5, 5.), nround)

        if (L, H) not in board_cases:
            board_cases.append((L, H))
    return board_cases

def generate_random_components(L, H, margin=0.1, nround=1):
    """ Generate a list of lists of a valid configuration
    Ex:
        comp_ls = [D0, C0, L0, S0]
    """
    lay_ls = []
    c = 0
    while c < 4:
        x, y = round(random.uniform(margin, L), nround), round(random.uniform(margin, H), nround)
        if is_component_inside(L, H, x, y, margin=margin) and c == 0:
            lay_ls.append((x, y))
            c += 1
        elif is_component_inside(L, H, x, y, margin=margin) and c != 0:
            if (x, y) not in lay_ls:
                lay_ls.append((x, y))
                c += 1
    return lay_ls


def monte_carlo_components(n_points, L, H, margin=0.1, nround=1):
    comp_ls = []
    c = 0
    while c <= n_points:
        lay_ls = generate_random_components(L, H, margin=margin, nround=nround)
        if lay_ls not in comp_ls:
            comp_ls.append(lay_ls)
            c += 1
    return comp_ls

def comp2dict(L, H, comp):
    """ Set L, H and components coordinates in a dictionary """
    design_parameters = {
    "board_width": L,           # 3
    "board_height" : H,         # 1
    "L_x": comp[0][0],
    "L_y": comp[0][1],
    "D_x": comp[1][0],
    "D_y": comp[1][1],
    "C_x": comp[2][0],
    "C_y": comp[2][1],
    "S_x": comp[3][0],
    "S_y": comp[3][1]
    }
    rel_dist_dict = {'l_LD': compute_euclidean_dist(comp[0], comp[1]),
                     'l_LC': compute_euclidean_dist(comp[0], comp[2]),
                     'l_LS': compute_euclidean_dist(comp[0], comp[3]),
                     'l_DC': compute_euclidean_dist(comp[1], comp[2]),
                     'l_DS': compute_euclidean_dist(comp[1], comp[3]),
                     'l_CS': compute_euclidean_dist(comp[2], comp[3])}

    return design_parameters, rel_dist_dict

def compute_euclidean_dist(X1, X2):
    """ Computes the euclidean distance given to tuples or lists X1 and X2 """
    d = np.sqrt((X1[0] - X2[0])**2 + (X1[1] - X2[1])**2)
    return d

def save_results(file):
    try:
        os.makedirs('results/')
    except:
        print('Directory already exists')
    n_file = len(os.listdir('results'))

    file_name = 'database_' + str(n_file) + '.pkl'
    print('Writing your results ...')
    with open('results/' + file_name, 'wb') as output:
        pickle.dump(file, output, pickle.HIGHEST_PROTOCOL)
    print('Done')

def compute_area(x1, y1, x2, y2, x3, y3, x4, y4):
    area = 0.5 * abs(
        (x1 * y2 + x2 * y3 + x3 * y4 + x4 * y1) -
        (y1 * x2 + y2 * x3 + y3 * x4 + y4 * x1)
    )
    return area

def compute_perimeter(x1, y1, x2, y2, x3, y3, x4, y4):
    # Compute the length of each side
    side1 = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    side2 = math.sqrt((x3 - x2) ** 2 + (y3 - y2) ** 2)
    side3 = math.sqrt((x4 - x3) ** 2 + (y4 - y3) ** 2)
    side4 = math.sqrt((x1 - x4) ** 2 + (y1 - y4) ** 2)

    # Compute the perimeter by summing all sides
    perimeter = side1 + side2 + side3 + side4
    return perimeter

#TODO
class Board_Layout:
    def __init__(self, L, H):
        pass


if __name__ == '__main__':

    # User input
    L, H = (3, 1)   # Board size
    n_points = 10000  # Number of sampling random points

    # Generate list of random configurations
    comp_ls = monte_carlo_components(n_points, 3, 1, nround=1)

    data = {}
    count = 0

    for i in range(n_points):
        data[i] = {}
        data[i]['layout'] = comp_ls[i]
        temp_des_par, temp_rel_dist = comp2dict(L, H, comp_ls[i])
        for k, v in temp_rel_dist.items():
            data[i][k] = v

        #
        # data[i]['rel_dist'] = temp_rel_dist
        data[i]['status'] = is_device_safe(temp_des_par)
        data[i]['therm'] = is_thermal_cycling_safe(temp_des_par)
        data[i]['cap'] = is_capacitor_safe(temp_des_par)
        data[i]['area'] = compute_area(comp_ls[i][0][0], comp_ls[i][0][1],
                                       comp_ls[i][1][0], comp_ls[i][1][1],
                                       comp_ls[i][2][0], comp_ls[i][2][1],
                                       comp_ls[i][3][0], comp_ls[i][3][1])
        data[i]['perim'] = compute_perimeter(comp_ls[i][0][0], comp_ls[i][0][1],
                                               comp_ls[i][1][0], comp_ls[i][1][1],
                                               comp_ls[i][2][0], comp_ls[i][2][1],
                                               comp_ls[i][3][0], comp_ls[i][3][1])

        if data[i]['status'] is True:
            count += 1

    print('{:d} were found from {:d} \n'
          'Successful percentage {:.2f}'.format(count, n_points, (count/n_points)*100))

    save_results(data)

#%%
    save_results(data)













