import cv2

import BinaryEncodingInterpreter
import PointCloudConstructor
import ContourReader
import ImageFunctions
import os
import glob
import pickle

show_plot = False


def images_import():
    img_dir = r'C:\Users\lesta\PycharmProjects\StructuredLightScanner\TestImages\Monkey'
    data_path = os.path.join(img_dir, '*g')
    files = glob.glob(data_path)
    horiz = []
    vert = []
    for f1 in files:
        #print(f1, f1[-6])
        img = cv2.imread(f1)
        if f1[-6] == 'H':
            horiz.append(img)
        if f1[-6] == 'V':
            vert.append(img)
    return horiz, vert

def images_import_blank():
    img_dir = r'C:\Users\lesta\PycharmProjects\StructuredLightScanner\TestImages\Blank'
    data_path = os.path.join(img_dir, '*g')
    files = glob.glob(data_path)
    horiz = []
    vert = []
    for f1 in files:
        #print(f1, f1[-6])
        img = cv2.imread(f1)
        if f1[-6] == 'H':
            horiz.append(img)
        if f1[-6] == 'V':
            vert.append(img)
    return horiz, vert


def images_to_binary(data):
    binary_images = []
    for image in data:
        img_bi = ImageFunctions.convert_to_binary(image)
        binary_images.append(img_bi)
    return binary_images

def pickle_dump(contour_list, filename):
    full_list = []
    for contour in contour_list:
        little_list = [contour.x_reduced, contour.y_reduced]
        full_list.append(little_list)
    with open(filename, 'wb') as fp:
        pickle.dump(full_list, fp)


def import_background():
    blank_horiz, blank_vert = images_import_blank()
    blank_binary_images_v = images_to_binary(blank_vert)
    blank_contour_list_v = BinaryEncodingInterpreter.code_cracker(blank_binary_images_v)
    pickle_dump(blank_contour_list_v, 'BlankFile')
    return blank_contour_list_v


def import_shape():
    horiz, vert = images_import()
    binary_images_v = images_to_binary(vert)
    contour_list_v = BinaryEncodingInterpreter.code_cracker(binary_images_v)
    pickle_dump(contour_list_v, 'MonkeyShapeFile')
    return contour_list_v


def main():
    blank_contour_list = import_background()
    print('Blank calibration images successfully imported')
    shape_contour_list = import_shape()
    print('Shape images successfully imported')
    print('Generating point cloud...')
    PointCloudConstructor.find_3D_shape_vert(blank_contour_list, shape_contour_list)


if __name__ == "__main__":
    main()