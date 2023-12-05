import utility
import canny_edge_detector as ced

imgs = utility.load_data(dir_name='images')
utility.visualize(imgs, 'gray')

detector = ced.cannyEdgeDetector(imgs, sigma=1.4, kernel_size=5, lowthreshold=0.09, highthreshold=0.17, weak_pixel=100)

imgs_final = detector.detect()

edges = imgs_final[0]



type(edges)

plot_points = []

utility.visualize(imgs_final,'gray')

for y in range(len(edges)-1):
    for x in range(len(edges[0])-1):
        if edges[y][x] > 0:
            plot_points.append((x,y))

print(plot_points)