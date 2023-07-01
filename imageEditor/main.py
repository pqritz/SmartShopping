from PIL import Image, ImageDraw, ImageFont


def __init__(path, points, color, size, pathOut, fontSize):
    image = Image.open(path)
    for p in points:
        add_marker(image, p, color, size, "", (0, 0), fontSize)
    image.save(pathOut)


def add_marker(image, position, color, size, text, textPos, fontSize):
    draw = ImageDraw.Draw(image)

    width, height = image.size
    marker_x, marker_y = position
    marker_x = int(marker_x * width)
    marker_y = int(marker_y * height)
    font = ImageFont.truetype("arial.ttf", fontSize)
    text_width, text_height = draw.textsize(text, font=font)
    position_x, position_y = textPos

    draw.text((position_x, position_y), text, font=font, fill=(255, 255, 255))

    marker_radius = int(size * min(width, height))
    marker_center = (marker_x, marker_y)
    marker_start_angle = 180  # Start angle for the half circle (180 degrees)
    marker_end_angle = 0  # End angle for the half circle (0 degrees)
    marker_box = [
        (marker_center[0] - marker_radius, marker_center[1] - marker_radius),
        (marker_center[0] + marker_radius, marker_center[1] + marker_radius)
    ]
    draw.pieslice(marker_box, start=marker_start_angle, end=marker_end_angle, fill=color)

    triangle_size = int(size * min(width, height))
    points = [
        (marker_center[0], marker_center[1] + triangle_size * 2),
        (marker_center[0] - triangle_size, marker_center[1]),
        (marker_center[0] + triangle_size, marker_center[1])
    ]
    draw.polygon(points, fill=color)
    # Save the modified image
    # return image