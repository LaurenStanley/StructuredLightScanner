import numpy as np
from matplotlib import pyplot as plt
from matplotlib import gridspec as gs
from matplotlib.pyplot import cm

# Input angle between the projector and the camera plane
camera_angle = -15
# Rather than calculating each loop
camera_angle_calc = np.tan(camera_angle)


def find_3D_shape(contour_list, height, width):
    # Create 3D Plot
    fig2 = plt.figure()
    ax2 = plt.axes(projection='3d')
    ax2.set_title('3D Plot')
    ax2.set_xlim(0, width)
    ax2.set_xlabel('X')
    ax2.set_ylim(-width/40, width/40)
    ax2.set_ylabel('Y')
    ax2.set_zlim(0, height)
    ax2.set_zlabel('Z')
    for j in range(len(contour_list)-1):
        # Get line of best fit from the top part of each contour. In this case I am assuming the object doesnt reach the
        # top of the screen. In the future, this will be replaced by a calibration image with no object.
        # for both horizontal and vertical in existing workspace (scanner space)
        m, b = np.polyfit(contour_list[j].y[10:400], contour_list[j].x[10:400], 1)
        yfit = np.linspace(0, 600, 100)
        xfit = m*yfit+b

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


        # Plot points
        ax2.scatter(x, y, z)

    plt.pause(10)
    plt.savefig('3D_Plot.png')
    ax2.clear()


    #fig = plt.figure(figsize=(5, 5))
    #gs1 = gs.GridSpec(nrows=1, ncols=2)
    #ax0 = fig.add_subplot(gs1[:, 0])
    #ax1 = fig.add_subplot(gs1[:, 1])
    #ax0.scatter(contour_list[0].x, contour_list[0].y)
    #ax0.plot(xfit, yfit)
    #ax1.plot(y, contour_list[0].y)
    #plt.pause(1)




