def direction_pixel(angle):
    direction = 0
    if angle%180 == 0:
        direction_pixel = [3, 5]
    elif angle%180 == 45 :
        direction_pixel = [0, 8]
    elif angle%180 == 90 :
        direction_pixel = [1, 7]
    elif angle%180 == 135:
        direction_pixel = [2, 6]
    return direction_pixel
