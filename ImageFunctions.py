import cv2
import nump as np

show_images = False


def image_display(name, image):
    if show_images:
        cv2.imshow(name, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


# Convert image to grayscale
def convert_to_grayscale(image):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_display('Grayscale', img_gray)

    return img_gray


# Convert image to binary using the mean intensity of the grayscale image
def convert_to_binary(image):
    img_gray = convert_to_grayscale(image)
    rows_mean_values = []
    for i in range(len(img_gray)):
        row_mean_value = np.mean(img_gray[i])
        rows_mean_values.append(row_mean_value)
    overall_mean_value = int(np.mean(rows_mean_values)*1.7)
    ret, img_bi = cv2.threshold(img_gray, overall_mean_value, 255, cv2.THRESH_BINARY_INV)
    image_display('Binary', img_bi)

    # Invert Binary Image
    imagem = cv2.bitwise_not(img_bi)
    image_display('Binary', imagem)
    return img_bi

