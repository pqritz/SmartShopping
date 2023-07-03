import cv2
import numpy as np

def find_non_white_pixel_coordinates(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Define the threshold value for white pixels
    threshold = 240

    # Iterate over each pixel and check if it is non-white
    pixel_coordinates = []
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if gray_image[y, x] < threshold:
                pixel_coordinates.append((x, y))

    return pixel_coordinates

def organize_coordinates(coordinates):
    organized_coordinates = {}
    for i, coord in enumerate(coordinates):
        index = i + 1
        x, y = coord
        organized_coordinates[str(index)] = {"x": x, "y": y}
    return organized_coordinates

# Example usage
image_path = 'C:/Users/morit/Desktop/Kibus/website/json/stores/points.png'
non_white_pixel_coordinates = find_non_white_pixel_coordinates(image_path)
coords = organize_coordinates(non_white_pixel_coordinates)
