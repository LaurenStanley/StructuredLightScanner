import numpy as np
from matplotlib import pyplot as plt
from matplotlib import gridspec as gs
import pickle

def find_3D_shape_vert(blank_list, shape_list):
    # Input angle between the projector and the camera plane
    camera_angle = -15
    camera_angle_calc = np.tan(camera_angle)

    # Create 3D Plot
    ax2 = plt.axes(projection='3d')
    ax2.set_title('3D Plot')
    #ax2.set_xlim(0, width)
    ax2.set_xlabel('X')
    #ax2.set_ylim(-100, 50)
    ax2.set_ylabel('Y')
    #ax2.set_zlim(0, height)
    ax2.set_zlabel('Z')
    x_list_raw = []
    y_list_raw = []
    z_list_raw = []
    for j in range(len(shape_list)):
        m, b = np.polyfit(blank_list[j].y_reduced, blank_list[j].x_reduced, 1)
        yfit = np.linspace(0, 1000, 100)
        xfit = m*yfit+b

        x = []
        y = []
        z = []

        # Each 3D point is calculated via distortion from what the line would be with no object there.
        # Axes are wrt the projector. Z is up here, not out like you expect from most camera axes.
        for i in range(len(shape_list[j].x_reduced)):
            d_value = shape_list[j].x_reduced[i] - (m * shape_list[j].y_reduced[i] + b)
            x.append(shape_list[j].x_reduced[i])
            z.append(shape_list[j].y_reduced[i])
            y.append(-d_value/camera_angle_calc)

        x_list_raw.append(x)
        y_list_raw.append(y)
        z_list_raw.append(z)
    x_list = []
    y_list = []
    z_list = []

    for j in range(len(x_list_raw)):
        x, y, z = find_anomalies(x_list_raw[j], y_list_raw[j], z_list_raw[j])
        x_list.append(x)
        y_list.append(y)
        z_list.append(z)
    x_list, y_list, z_list = find_anomalies_bulk(x_list, y_list, z_list)

    for i in range(len(x_list)):
        ax2.scatter(x_list[i], y_list[i], z_list[i])

    with open(r'C:\Users\lesta\PycharmProjects\StructuredLightScanner\Point_Cloud.txt', 'w') as fp:
        fp.write("")
    with open(r'C:\Users\lesta\PycharmProjects\StructuredLightScanner\Point_Cloud.txt', 'a') as fp:
        for i in range(len(x_list)):
            # print(i)
            fp.write('{')
            for j in range(len(x_list[i])):
                # print(j)
                fp.write('{')
                fp.write(str(x_list[i][j]))
                fp.write(',')
                fp.write(str(y_list[i][j]))
                fp.write(',')
                fp.write(str(z_list[i][j]))
                fp.write('},')
            fp.seek(0, 2)  # seek to end of file; f.seek(0, os.SEEK_END) is legal
            fp.seek(fp.tell() - 1, 0)  # seek to the second last char of file; f.seek(f.tell()-2, os.SEEK_SET) is legal
            fp.truncate()
            fp.write('},')
        fp.seek(0, 2)  # seek to end of file; f.seek(0, os.SEEK_END) is legal
        fp.seek(fp.tell() - 2, 0)  # seek to the second last char of file; f.seek(f.tell()-2, os.SEEK_SET) is legal
        fp.truncate()
        fp.write('}')

    plt.savefig('3D_Plot.png')
    plt.pause(30)
    ax2.clear()

def find_anomalies_bulk(x,y,z):
    # define a list to accumlate anomalies
    x_flat = []
    for sublist in x:
        for item in sublist:
            x_flat.append(item)
    y_flat = []
    for sublist in y:
        for item in sublist:
            y_flat.append(item)
    z_flat = []
    for sublist in z:
        for item in sublist:
            z_flat.append(item)

    # Set upper and lower limit to 3 standard deviation
    x_std = np.std(x_flat)
    x_mean = np.mean(x_flat)
    x_cut_off = x_std * 2
    y_std = np.std(y_flat)
    y_mean = np.mean(y_flat)
    y_cut_off = y_std * 2
    z_std = np.std(z_flat)
    z_mean = np.mean(z_flat)
    z_cut_off = z_std * 2

    x_lower_limit = x_mean - x_cut_off
    x_upper_limit = x_mean + x_cut_off
    y_lower_limit = y_mean - 2*y_cut_off
    y_upper_limit = y_mean + y_cut_off
    z_lower_limit = z_mean - z_cut_off
    z_upper_limit = z_mean + z_cut_off
    # Generate outliers
    x_good = []
    y_good = []
    z_good = []

    for j in range(len(x)):
        x_good1 = []
        y_good1 = []
        z_good1 = []
        for i in range(len(x[j])):
            if x[j][i] < x_upper_limit and x[j][i] > x_lower_limit:
                if y[j][i] < y_upper_limit and y[j][i] > y_lower_limit:
                    if z[j][i] < z_upper_limit and z[j][i] > z_lower_limit:
                        x_good1.append(x[j][i])
                        y_good1.append(y[j][i])
                        z_good1.append(z[j][i])
        x_good.append(x_good1)
        y_good.append(y_good1)
        z_good.append(z_good1)
    return x_good, y_good, z_good


def find_anomalies(x,y,z):
    # define a list to accumlate anomalies
    x_good = []
    y_good = []
    z_good = []

    # Set upper and lower limit to 3 standard deviation
    x_std = np.std(x)
    x_mean = np.mean(x)
    x_cut_off = x_std * 2
    y_std = np.std(y)
    y_mean = np.mean(y)
    y_cut_off = y_std * 2
    z_std = np.std(z)
    z_mean = np.mean(z)
    z_cut_off = z_std * 2

    x_lower_limit = x_mean - x_cut_off
    x_upper_limit = x_mean + x_cut_off
    y_lower_limit = y_mean - y_cut_off
    y_upper_limit = y_mean + y_cut_off
    z_lower_limit = z_mean - z_cut_off
    z_upper_limit = z_mean + z_cut_off
    # Generate outliers
    for i in range(len(x)):
        if x[i] < x_upper_limit and x[i] > x_lower_limit:
            if y[i] < y_upper_limit and y[i] > y_lower_limit:
                if z[i] < z_upper_limit and z[i] > z_lower_limit:
                    x_good.append(x[i])
                    y_good.append(y[i])
                    z_good.append(z[i])
    return x_good, y_good, z_good
