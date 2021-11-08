import cv2
import processor
import ContourReader
import ImageFunctions

show_plot = False


# Import Image
def image_import():
    # Test images
    # path = r'C:\Users\lesta\PycharmProjects\StructuredLightScanner\TestImages\StackTest.png'
    # path = r'C:\Users\lesta\PycharmProjects\StructuredLightScanner\TestImages\man (Gray)\v1\36.bmp'
    # path = r'C:\Users\lesta\PycharmProjects\StructuredLightScanner\TestImages\TroughTest.png'
    # path = r'C:\Users\lesta\PycharmProjects\StructuredLightScanner\TestImages\Figures\Frame7.png'
    path = r'C:\Users\lesta\PycharmProjects\StructuredLightScanner\TestImages\PaintAngle.png'

    img = cv2.imread(path)

    ImageFunctions.image_display('Original', img)
    return img


def main():
    image = image_import()
    img_bi = ImageFunctions.convert_to_binary(image)

    maxima_mask = ContourReader.local_maxima_from_binary(img_bi)
    contour_list = ContourReader.connected_contours(maxima_mask, image.shape[0], image.shape[1], show_plot)
    processor.find_3D_shape(contour_list, image.shape[0], image.shape[1])


if __name__ == "__main__":
    main()