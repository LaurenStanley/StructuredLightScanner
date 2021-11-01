import cv2
from matplotlib import pyplot as plt
from matplotlib import gridspec as gs
from matplotlib.pyplot import cm
import numpy as np
import scipy.ndimage as ndimage
import processor

show_images = False
show_plot = False

def image_display(name, image):
    if show_images:
        cv2.imshow(name, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


# Import Image
def image_import():
    # Other test images
    # path = r'C:\Users\lesta\PycharmProjects\StructuredLightScanner\TestImages\StackTest.png'
    # path = r'C:\Users\lesta\PycharmProjects\StructuredLightScanner\TestImages\man (Gray)\v1\36.bmp'
    #path = r'C:\Users\lesta\PycharmProjects\StructuredLightScanner\TestImages\TroughTest.png'
    path = r'C:\Users\lesta\PycharmProjects\StructuredLightScanner\TestImages\Figures\Frame7.png'
    #path = r'C:\Users\lesta\PycharmProjects\StructuredLightScanner\TestImages\PaintAngle.png'

    img = cv2.imread(path)

    image_display('Original', img)
    return img


# Convert image to grayscale
def convert_to_grayscale(image):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_display('Grayscale', img_gray)
    return img_gray


# Convert image to binary using the mean intensity of the grayscale image
def convert_to_binary(img_gray):
    rows_mean_values = []
    for i in range(len(img_gray)):
        row_mean_value = np.mean(img_gray[i])
        rows_mean_values.append(row_mean_value)
    overall_mean_value = int(np.mean(rows_mean_values)*1.7)
    ret, img_bi = cv2.threshold(img_gray, overall_mean_value, 255, cv2.THRESH_BINARY_INV)
    image_display('Binary', img_bi)
    # Invert Binary Image
    #imagem = cv2.bitwise_not(img_bi)
    #cv2.imshow('Binary', imagem)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return img_bi


# OpenCV Contour Detect - this was a test of a different possible method
def contour_detect(image, img_bi):
    contours, hierarchy = cv2.findContours(img_bi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_contour = cv2.drawContours(image, contours, -1, (0,255,75), 2)
    image_display('Contours', img_contour)

#or intensity filtered images
def local_maxima(image):
    # Close Contours binary areas, blur to reduce noise -
    img_bi_closed = cv2.morphologyEx(image, cv2.MORPH_CLOSE, np.ones((2, 2)))
    cv2.imshow('Closed 1', img_bi_closed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    img_bi_closed_blurred = cv2.GaussianBlur(img_bi_closed, (5, 5), 0)

    # image_display('Closed, Blurred', img_bi_closed_blurred)

    img_bi_closed_blurred = img_bi_closed_blurred.sum(axis=2)
    #this is the juice - find the local maxima by column, return as a booleam
    mx = np.zeros(img_bi_closed_blurred.shape)
    lm = ndimage.filters.maximum_filter(img_bi_closed_blurred, footprint=np.ones((1, 10)))
    msk = (img_bi_closed_blurred == lm)

    #Convert to image
    msk = msk.astype(np.uint8)  #convert to an unsigned byte
    msk *= 255

    image_display('Mask', msk)

    return msk

def local_maxima2(image):
    # For binary filtered images
    # Close Contours binary areas, blur to reduce noise
    img_bi_closed = cv2.morphologyEx(image, cv2.MORPH_CLOSE,np.ones((2,2)))
    image_display('Closed', img_bi_closed)

    img_bi_closed_blurred = cv2.GaussianBlur(img_bi_closed, (5,5),0)

    #image_display('Closed, Blurred', img_bi_closed_blurred)

    # This is the juice - find the local maxima by column, return as a booleam
    mx = np.zeros(img_bi_closed_blurred.shape)
    #for c in range(1, len(img_bi_closed_blurred)):

    lm = ndimage.filters.maximum_filter(img_bi_closed_blurred, footprint=np.ones((1, 6)))
    msk1 = (img_bi_closed_blurred != mx)
    msk = (msk1 == lm)

    # Convert to image
    msk = msk.astype(np.uint8)  # convert to an unsigned byte
    msk *= 255

    image_display('Mask', msk)
    return msk


class Contour:
    contour = 'contour'

    def __init__(self, label, x, y):
        self.label = label
        self.x = x
        self.y = y


def connected_contours(msk, height, width):
    # Get connected contours - as pixels which are in contact
    output = cv2.connectedComponentsWithStats(
        msk, 4)
    (numLabels, labels, stats, centroids) = output
    print(numLabels)

    label_hue = np.uint8(179*labels/np.max(labels))
    blank_ch = 255*np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

    # cvt to BGR for display
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

    # set bg label to black
    labeled_img[label_hue==0] = 0

    image_display('labeled.png', labeled_img)

    contour_list = []
    for label in range(numLabels):
        contour = Contour(str(label), [], [])
        for i in range(len(labels)):
            for j in range(len(labels[i])):
                if labels[i][j] == label+1:
                    contour.x.append(j)
                    contour.y.append(len(labels)-i)
        contour_list.append(contour)

    if show_plot:
        fig = plt.figure(figsize=(5, 5))
        gs1 = gs.GridSpec(nrows=1, ncols=1)
        ax0 = fig.add_subplot(gs1[:, 0])
        color = cm.gnuplot(np.linspace(0, 1, len(contour_list)))
        for i,c in zip(range(len(contour_list)), color):
            ax0.scatter(contour_list[i]. x,contour_list[i].y, color=c)
        ax0.axis([0, width, 0, height])
        plt.pause(20)
    return contour_list

def main():
    image = image_import()
    img_gray = convert_to_grayscale(image)
    img_bi = convert_to_binary(img_gray)
    #maxima_mask = local_maxima(image)
    maxima_mask = local_maxima2(img_bi)
    contour_list = connected_contours(maxima_mask, image.shape[0], image.shape[1])
    processor.find_3D_shape(contour_list)

if __name__ == "__main__":
    main()