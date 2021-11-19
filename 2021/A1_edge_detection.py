from A1_image_filtering import *
import cv2
import numpy as np
import time

lenna_img = cv2.imread('lenna.png', cv2.IMREAD_GRAYSCALE)
shapes_img = cv2.imread('shapes.png', cv2.IMREAD_GRAYSCALE)

# 2-1
gaussian = get_gaussian_filter_2d(7, 1.5)
lenna_gauss = cross_correlation_2d(lenna_img, gaussian)
shapes_gauss = cross_correlation_2d(shapes_img, gaussian)

# 2-2
def compute_img_gradient(img):
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

    derivative_x = cross_correlation_2d(img, sobel_x)
    derivative_y = cross_correlation_2d(img, sobel_y)

    mag = np.sqrt(np.square(derivative_x) + np.square(derivative_y))

    dir = np.arctan2(derivative_y, derivative_x)
    return mag, dir

## (d)
# lenna.png
tic = time.time()

len_mag, len_dir = compute_img_gradient(lenna_gauss)

tac = time.time()
print(f'lenna magnitude computational time: {tac - tic}')

cv2.imshow('lenna magnitude', len_mag)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('./result/part_2_edge_raw_lenna.png', len_mag)

# shapes.png
tic = time.time()

shp_mag, shp_dir = compute_img_gradient(shapes_gauss)

tac = time.time()
print(f'shapes magnitude computational time: {tac - tic}')

cv2.imshow('shapes magnitude', shp_mag)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('./result/part_2_edge_raw_shapes.png', shp_mag)


# 2-3
from direction_code import *

def non_maximum_suppression(mag, dir):
    dir = np.rad2deg(dir)
    dir[dir < 0] += 360

    quan_dir = np.round(dir / 45) * 45
    quan_dir[quan_dir == 360] = 0

    h, w = mag.shape
    suppressed_mag = np.zeros([h, w])

    for i in range(1, h - 1):
        for j in range(1, w - 1):
            mag_8 = mag[i - 1: i + 2, j - 1: j + 2].flatten()
            pix_idx = direction_pixel(quan_dir[i, j])

            sur_mag1 = mag_8[pix_idx[0]]
            sur_mag2 = mag_8[pix_idx[1]]

            suppressed_mag[i, j] = mag_8[4] if mag_8[4] >= np.max([sur_mag1, sur_mag2]) else 0

    return suppressed_mag

## (d)
# lenna.png
tic = time.time()
len_nms = non_maximum_suppression(len_mag, len_dir)
tac = time.time()
print(f'lenna NMS computation time : {tac - tic}')

cv2.imshow('lenna NMS', len_nms)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('./result/part_2_edge_sup_lenna.png', len_nms)

# shapes.png
# lenna.png
tic = time.time()
shp_nms = non_maximum_suppression(shp_mag, shp_dir)
tac = time.time()
print(f'shapes NMS computation time : {tac - tic}')

cv2.imshow('shpaes NMS', shp_nms)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('./result/part_2_edge_sup_shapes.png', shp_nms)