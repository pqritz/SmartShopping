import cv2
import numpy as np

def find_color_cluster_coordinates(image_path, lower_color, upper_color):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to the HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the color range
    lower_bound = np.array(lower_color, dtype=np.uint8)
    upper_bound = np.array(upper_color, dtype=np.uint8)

    # Create a mask based on the color range
    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through each contour and calculate the center coordinate
    color_cluster_coordinates = []
    for contour in contours:
        # Calculate the center of the contour
        M = cv2.moments(contour)
        if M["m00"] != 0:
            x = int(M["m10"] / M["m00"])
            y = int(M["m01"] / M["m00"])
            # Adjust the y-coordinate to match the top-left origin
            adjusted_y = hsv_image.shape[0] - y
            color_cluster_coordinates.append((x, adjusted_y))

    # Display the converted image
    cv2.imshow('Converted Image', hsv_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return color_cluster_coordinates


def organize_coordinates(coordinates):
    organized_coordinates = {}
    for i, coord in enumerate(coordinates):
        index = i + 1
        x, y = coord
        organized_coordinates[str(index)] = {"x": x, "y": y}
    return organized_coordinates

# Example usage


# Example usage
image_path = 'C:/Users/morit/Desktop/Kibus/website/json/stores/Unbenannt.png'
lower_color = [0, 100, 99]  # Adjusted lower HSV values for red
upper_color = [1, 255, 255]  # Adjusted upper HSV values for red

coordinates = find_color_cluster_coordinates(image_path, lower_color, upper_color)
organized = organize_coordinates(coordinates)
print(organized)
print(coordinates)
print(len(coordinates))