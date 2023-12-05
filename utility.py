import numpy as np
import skimage
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
import os
import scipy.misc as sm

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

    # Multiply all x and y values by their corresponding ratios.
    # Add 2 to each y value. We need a buffer of 2 centimeters
    # so penpal doesn't run into itself
    for i, coordinate in enumerate(points):
        coordinate[0] *= X_SCALE
        coordinate[1] *= Y_SCALE
        coordinate[1] += 2


def copyToPositionsTxt(points):
    file = open("positions.txt", "w")
    for i, coordinate in enumerate(points):
        file.write(f"{coordinate[0]},{coordinate[1]}")
        if i < len(points)-1:
            file.write("\n")
