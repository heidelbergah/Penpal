import numpy as np
import skimage
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
import os
import scipy.misc as sm
from itertools import groupby, product

def rgb2gray(rgb):

    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray

def load_data(dir_name = 'faces_imgs'):    
    '''
    Load images from the "faces_imgs" directory
    Images are in JPG and we convert it to gray scale images
    '''
    imgs = []
    for filename in os.listdir(dir_name):
        if os.path.isfile(dir_name + '/' + filename):
            img = mpimg.imread(dir_name + '/' + filename)
            img = rgb2gray(img)
            imgs.append(img)
    return imgs


def manhattan(tup1, tup2):
    return abs(tup1[0] - tup2[0]) + abs(tup1[1] - tup2[1])


def group(test_list):
    # Group Adjacent Coordinates
    # Using product() + groupby() + list comprehension
    man_tups = [sorted(sub) for sub in product(test_list, repeat = 2)
    									if manhattan(*sub) == 1]
 
    res_dict = {ele: {ele} for ele in test_list}
    for tup1, tup2 in man_tups:
        res_dict[tup1] |= res_dict[tup2]
        res_dict[tup2] = res_dict[tup1]
 
    res = [[*next(val)] for key, val in groupby(
    		sorted(res_dict.values(), key = id), id)]
 
    # converting tuples to numpy arrays
    res = [np.array(sub) for sub in res]
 
    # sorting numpy arrays lexicographically
    res = sorted(res, key=lambda x: tuple(x[:,0]))
 
    #converting numpy arrays back to tuples
    res = [tuple(map(tuple, sub)) for sub in res]
    return res


def visualize(imgs, format=None, gray=False):
    plt.figure(figsize=(20, 40))
    for i, img in enumerate(imgs):
        if img.shape[0] == 3:
            img = img.transpose(1,2,0)
        plt_idx = i+1
        plt.subplot(2, 2, plt_idx)
        plt.imshow(img, format)
    plt.show()


def fitToScale(armLength, points):
    # Some trig to find the maximum x and y values penpal can reach
    max_plot_x = (np.sqrt(2)*(armLength*2))/2
    max_plot_y = max_plot_x

    max_plot_y -= 2 # Shift values up by 2 at end of program

    # Find max x and y values in list of coordinates. This
    # will tell us the drawing space needed
    X_MAX = max(points, key=lambda point: point[0])[0]
    Y_MAX = max(points, key=lambda point: point[1])[1]

    # Generate a scale for penpal to draw. Penpal needs coordinates
    # in terms of centimeters, not pixels. This finds the according
    # conversion ratio for x and y values
    X_SCALE = float(max_plot_x / X_MAX)
    Y_SCALE = float(max_plot_y / Y_MAX)

    return [X_SCALE, Y_SCALE]


def copyToPositionsTxt(points):
    file = open("positions.txt", "w")
    X_SCALE, Y_SCALE = fitToScale(10.5, points)
    points = group(points)

    file.write("t\n")
    for i in range(len(points)-1):
        for j in range(len(points[i])-1):
            if(j == 0):
                x = points[i][j][0] * X_SCALE
                y = (points[i][j][1] * Y_SCALE) + 2
                file.write(f"{x},{y}\n")
                file.write("t\n")
            else:
                x = points[i][j][0] * X_SCALE
                y = (points[i][j][1] * Y_SCALE) + 2
                file.write(f"{x},{y}\n")
        file.write("t\n")
    file.close()