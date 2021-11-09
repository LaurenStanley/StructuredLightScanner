import numpy as np
from matplotlib import pyplot as plt
from matplotlib import gridspec as gs
from matplotlib.pyplot import cm
import cv2
import ImageFunctions

show_plot = True

class Binary_Contour:
    binary_contour = 'binary_contour'

    def __init__(self, label, x, y):
        self.label = label
        self.x = x
        self.y = y


def code_cracker(images):
    new_image = []
    label_list = []
    for j in range(len(images[1])):
    #for j in range(10):
        new_row = []
        for k in range(len(images[1][1])):
        #for k in range(10):
            binary_multi = 1
            binary_value = 0
            for i in range(len(images)):
                pixel = images[i][j][k]
                binary_value += pixel/255 * binary_multi
                binary_multi = binary_multi * 10
            pixel_value = (int(str(int(binary_value)), 2))
            new_row.append(pixel_value)
            if pixel_value not in label_list:
                label_list.append(pixel_value)
        new_image.append(new_row)
    print(len(new_image))
    label_list.sort()

    del label_list[0]
    del label_list[-1]
    #del label_list[10:]
    print(label_list)
    new_image2 = np.array(new_image,dtype = np.uint32)
    label_hue = np.uint8(179 * new_image2/ np.max(label_list))
    print(len(label_hue))
    blank_ch = 255 * np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

    # cvt to BGR for display
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

    # set bg label to black
    labeled_img[label_hue == 0] = 0

    ImageFunctions.image_display('labeled.png', labeled_img)
    binary_contour_list = []
    for label in label_list:
        binary_contour = Binary_Contour(str(label), [], [])
        for i in range(len(new_image)):
            for j in range(len(new_image[i])):
                if new_image[i][j] == label:
                    binary_contour.x.append(j)
                    binary_contour.y.append(i)
        binary_contour_list.append(binary_contour)

    print(len(binary_contour_list))
    if show_plot:
        fig = plt.figure(figsize=(5, 5))
        gs1 = gs.GridSpec(nrows=1, ncols=1)
        ax0 = fig.add_subplot(gs1[:, 0])
        #color = cm.gnuplot(np.linspace(0, 1, len(binary_contour_list)))
        color = cm.rainbow(np.linspace(0, 1, len(binary_contour_list)))
        for i, c in zip(range(len(binary_contour_list)), color):
            ax0.scatter(binary_contour_list[i].x, binary_contour_list[i].y, color=c,label=binary_contour_list[i].label)
        ax0.axis([0, images[0].shape[1], 0, images[0].shape[0]])
        ax0.legend()
        plt.pause(20)
    return binary_contour_list