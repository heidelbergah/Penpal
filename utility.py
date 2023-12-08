import numpy as np

Y_MAX = 0

def midpt(*args):
    xs,ys = 0,0
    for p in args:
        xs += p[0]
        ys += p[1]
    return xs/len(args),ys/len(args)


def distsum(*args):
    return sum([ ((args[i][0]-args[i-1][0])**2 + (args[i][1]-args[i-1][1])**2)**0.5 for i in range(1,len(args))])


def fitToScale(armLength, points):
    # Some trig to find the maximum x and y values penpal can reach
    max_plot_x = (np.sqrt(2)*(armLength*2))/2
    max_plot_y = max_plot_x

    max_plot_y -= 2 # Shift values up by 2 at end of program

    # Find max x and y values in list of coordinates. This
    # will tell us the drawing space needed
    global Y_MAX
    X_MAX = Y_MAX = 0
    for i in range(len(points)-1):
        for j in range(len(points[i])-1):
            if(X_MAX < points[i][j][0]):
                X_MAX = points[i][j][0]
            if(Y_MAX < points[i][j][1]):
                Y_MAX = points[i][j][1]


    # Generate a scale for penpal to draw. Penpal needs coordinates
    # in terms of centimeters, not pixels. This finds the according
    # conversion ratio for x and y values
    X_SCALE = float(max_plot_x / X_MAX)
    Y_SCALE = float(max_plot_y / Y_MAX)

    return [X_SCALE, Y_SCALE]

# Math domain error being caused by something in here!
def copyToPositionsTxt(points):
    file = open("positions.txt", "w")
    X_SCALE, Y_SCALE = fitToScale(10.5, points)

    for i in range(len(points)-1):
        for j in range(len(points[i])-1):
            if(j == 0):
                x = points[i][j][0] * X_SCALE
                y = (abs(points[i][j][1] - Y_MAX) * Y_SCALE) + 2
                file.write(f"{x},{y}\n")
                file.write("t\n")
            else:
                x = points[i][j][0] * X_SCALE
                y = (abs(points[i][j][1] - Y_MAX) * Y_SCALE) + 2
                file.write(f"{x},{y}\n")
        file.write("t\n")
    file.close()
