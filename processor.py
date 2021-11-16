import numpy as np
from matplotlib import pyplot as plt
from matplotlib import gridspec as gs

# Input angle between the projector and the camera plane
camera_angle = -15
# Rather than calculating each loop
camera_angle_calc = np.tan(camera_angle)


def find_3D_shape(contour_list, height, width):
    # Create 3D Plot
    ax2 = plt.axes(projection='3d')
    ax2.set_title('3D Plot')
    #ax2.set_xlim(0, width)
    ax2.set_xlabel('X')
    #ax2.set_ylim(-50, 500)
    ax2.set_ylabel('Y')
    #ax2.set_zlim(0, height)
    ax2.set_zlabel('Z')
    x_list = []
    y_list = []
    z_list = []
    for j in range(len(contour_list)-1):
    #for j in range(1):
        #print(j)
        # Get line of best fit from the top part of each contour. In this case I am assuming the object doesnt reach the
        # top of the screen. In the future, this will be replaced by a calibration image with no object.
        # for both horizontal and vertical in existing workspace (scanner space)
        m, b = np.polyfit(contour_list[j].y_reduced, contour_list[j].x_reduced, 1)
        #print(m,b)
        yfit = np.linspace(0, 1000, 100)
        xfit = m*yfit+b
        #fig = plt.figure(figsize=(5, 5))
        #gs1 = gs.GridSpec(nrows=1, ncols=1)
        #ax0 = fig.add_subplot(gs1[:, 0])
        #ax0.axis([0, width, 0, height])

        x = []
        y = []
        z = []

        # Each 3D point is calculated via distortion from what the line would be with no object there.
        # Axes are wrt the projector. Z is up here, not out like you expect from most camera axes.
        for i in range(len(contour_list[j].x)):
            d_value = contour_list[j].x[i] - (m * contour_list[j].y[i] + b)
            x.append(contour_list[j].x[1])
            z.append(contour_list[j].y[i])
            y.append(-d_value/camera_angle_calc)

        #ax0.scatter(xfit, yfit)
        #ax0.scatter(contour_list[j].x_reduced, contour_list[j].y_reduced)
        #ax0.scatter(x, z)
        #plt.pause(20)
        # Plot points
        x_list.append(x)
        y_list.append(y)
        z_list.append(z)
    for i in range(len(x_list)):
        ax2.scatter(x_list[i], y_list[i], z_list[i])

    plt.pause(30)
    plt.savefig('3D_Plot.png')
    ax2.clear()

