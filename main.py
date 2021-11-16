import cv2

import BinaryEncodingInterpreter
import processor
import ContourReader
import ImageFunctions
import os
import glob

show_plot = False


# Import Image
def image_import():
    # Test images
    # path = r'C:\Users\lesta\PycharmProjects\StructuredLightScanner\TestImages\StackTest.png'
    # path = r'C:\Users\lesta\PycharmProjects\StructuredLightScanner\TestImages\man (Gray)\v1\36.bmp'
    # path = r'C:\Users\lesta\PycharmProjects\StructuredLightScanner\TestImages\TroughTest.png'
    # path = r'C:\Users\lesta\PycharmProjects\StructuredLightScanner\TestImages\Figures\Frame7.png'
    # path = r'C:\Users\lesta\PycharmProjects\StructuredLightScanner\TestImages\PaintAngle.png'
    path = r'C:\Users\lesta\PycharmProjects\StructuredLightScanner\TestImages\Figures\Frame 1 - Try 1.png'
    img = cv2.imread(path)

    ImageFunctions.image_display('Original', img)
    return img

def images_import():
    #img_dir = r'C:\Users\lesta\PycharmProjects\StructuredLightScanner\TestImages\BinaryPaintTest2'
    img_dir = r'C:\Users\lesta\PycharmProjects\StructuredLightScanner\TestImages\Figures'
    data_path = os.path.join(img_dir, '*g')
    files = glob.glob(data_path)
    data = []
    for f1 in files:
        print(f1)
        img = cv2.imread(f1)
        data.append(img)
    data.reverse()
    return data


def images_to_binary(data):
    binary_images = []
    for image in data:
        img_bi = ImageFunctions.convert_to_binary(image)
        binary_images.append(img_bi)
    return binary_images

def contour_process(binary_images):
    contour_list = []
    for img_bi in binary_images:
        maxima_mask = ContourReader.local_maxima_from_binary(img_bi)
        contour_list.append(ContourReader.connected_contours(maxima_mask, img_bi.shape[0], img_bi.shape[1], show_plot))
    return contour_list


def main():
    data = images_import()
    # img_bi = ImageFunctions.convert_to_binary(image)
    binary_images = images_to_binary(data)
    #contour_process(binary_images)
    contour_list = BinaryEncodingInterpreter.code_cracker(binary_images)

    processor.find_3D_shape(contour_list, binary_images[0].shape[0], binary_images[0].shape[1])


if __name__ == "__main__":
    main()