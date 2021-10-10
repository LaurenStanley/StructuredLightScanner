import cv2
from matplotlib import pyplot as plt
from matplotlib import gridspec as gs
import numpy as np
import scipy.ndimage as ndimage


#Import Image
def image_import():
    #path = r'C:\Users\lesta\Downloads\2671.jpg'
    path = r'C:\Users\lesta\PycharmProjects\StructuredLightScanner\TestImages\StackTest.png'
    #path = r'C:\Users\lesta\PycharmProjects\StructuredLightScanner\TestImages\man (Gray)\v1\36.bmp'
    image = cv2.imread(path)
    #cv2.imshow('Source', image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return image


def convert_to_grayscale(image):
    #Convert Image to Grayscale
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('Grayscale', img_gray)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return img_gray


def convert_to_binary(img_gray):
    rows_mean_values = []
    for i in range(len(img_gray)):
        row_mean_value = np.mean(img_gray[i])
        rows_mean_values.append(row_mean_value)
    overall_mean_value = int(np.mean(rows_mean_values))
    ret, img_bi = cv2.threshold(img_gray, overall_mean_value, 255, cv2.THRESH_BINARY_INV)
    print(ret)
    cv2.imshow('Binary', img_bi)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return img_bi


def contour_detect(image, img_bi):
    #OpenCV Contour Detect - this was a test of a different possible method lol

    contours, hierarchy = cv2.findContours(img_bi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_contour = cv2.drawContours(image, contours, -1, (0,255,75), 2)
    cv2.imshow('Contours', img_contour)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def local_maxima(image):
    #Close Contours binary areas, blur to reduce noise
    img_bi_closed = cv2.morphologyEx(image, cv2.MORPH_CLOSE,np.ones((2,2)))
    #cv2.imshow('Closed', img_bi_closed)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    img_bi_closed_blurred = cv2.GaussianBlur(img_bi_closed, (5,5),0)

    #cv2.imshow('Closed, Blurred', img_bi_closed_blurred)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    img_bi_closed_blurred = img_bi_closed_blurred.sum(axis=2)
    #this is the juice - find the local maxima by column, return as a booleam
    mx = np.zeros(img_bi_closed_blurred.shape)
    #for c in range(1, len(img_bi_closed_blurred)):
    #lm = ndimage.filters.maximum_filter(img_bi_closed_blurred, footprint=np.ones((1,9)))
    #    msk = (img_bi_closed_blurred == lm)

    lm = ndimage.filters.maximum_filter(img_bi_closed_blurred, footprint=np.ones((10 ,1)))
    msk = (img_bi_closed_blurred == lm)


    #Convert to image
    msk = msk.astype(np.uint8)  #convert to an unsigned byte
    msk*=255

    cv2.imshow('Mask', msk)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return msk


def connected_contours(msk):
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

    cv2.imshow('labeled.png', labeled_img)
    cv2.waitKey()

    contour10x = []
    contour10y = []

    for i in range(len(labels)):
        for j in range(len(labels[i])):
            if labels[i][j] == 16:
                print(labels[i][j])
                contour10x.append(j)
                contour10y.append(i)


    fig = plt.figure(figsize=(5, 5))
    gs1 = gs.GridSpec(nrows=1, ncols=1)
    ax0 = fig.add_subplot(gs1[:, 0])
    ax0.scatter(contour10x,contour10y, color='green')
    ax0.axis([0, 300, 0, 300])
    plt.pause(10)

def main():
    image = image_import()
    img_gray = convert_to_grayscale(image)
    img_bi = convert_to_binary(img_gray)
    #contour_detect(image, img_bi)
    maxima_mask = local_maxima(image)
    connected_contours(maxima_mask)

if __name__ == "__main__":
    main()