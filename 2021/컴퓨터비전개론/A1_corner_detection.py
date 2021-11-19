import cv2
import numpy as np
from A1_image_filtering import *
import time
import matplotlib.pyplot as plt

lenna_img = cv2.imread('lenna.png', cv2.IMREAD_GRAYSCALE)
shapes_img = cv2.imread('shapes.png', cv2.IMREAD_GRAYSCALE)

# 3-1
gaussian = get_gaussian_filter_2d(7, 1.5)
lenna_gauss = cross_correlation_2d(lenna_img, gaussian)
shapes_gauss = cross_correlation_2d(shapes_img, gaussian)

# 3-2
def compute_corner_response(img):
    h, w = img.shape

    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

    derivative_x = cross_correlation_2d(img, sobel_x)
    derivative_y = cross_correlation_2d(img, sobel_y)

    derivative_x -= np.mean(derivative_x.flatten())
    derivative_y -= np.mean(derivative_y.flatten())

    window = np.ones((5, 5))

    M_1 = cross_correlation_2d(np.square(derivative_x), window)
    M_2 = cross_correlation_2d(derivative_x * derivative_y, window)
    M_4 = cross_correlation_2d(np.square(derivative_y), window)

    M = np.zeros((h, w, 2, 2))
    M[:, :, 0, 0] = M_1
    M[:, :, 0, 1] = M_2
    M[:, :, 1, 0] = M_2
    M[:, :, 1, 1] = M_4

    det_M = np.zeros((h, w))
    det_M = M[:, :, 0, 0] * M[:, :, 1, 1] - M[:, :, 0, 1] * M[:, :, 1, 0]

    tr_M = np.zeros((h, w))
    tr_M = M[:, :, 0, 0] + M[:, :, 1, 1]

    k = 0.04
    R = np.zeros((h, w))
    R = det_M - k * np.square(tr_M)

    R[R < 0] = 0.
    R /= np.max(R.flatten())

    return R

## (e)
# lenna.png
tic = time.time()
len_cor_res = compute_corner_response(lenna_gauss)
tac = time.time()

print(f'lenna corner response calculate time : {tac - tic}')
cv2.imshow('lenna corner', len_cor_res)
cv2.waitKey(0)
cv2.destroyAllWindows()
plt.imsave('./result/part_3_corner_raw_lenna.png', len_cor_res, cmap = 'gray')

# shapes.png
tic = time.time()
shp_cor_res = compute_corner_response(shapes_gauss)
tac = time.time()

print(f'shapes corner response calculate time : {tac - tic}')
cv2.imshow('shapes corner', shp_cor_res)
cv2.waitKey(0)
cv2.destroyAllWindows()
plt.imsave('./result/part_3_corner_raw_shapes.png', shp_cor_res, cmap = 'gray')

# 3-3
## (a)
# lenna.png
lenna_rgb = cv2.imread('lenna.png', cv2.IMREAD_COLOR)

b, g, r = lenna_rgb[:, :, 0], lenna_rgb[:, :, 1], lenna_rgb[:, :, 2]
gray = 0.299 * r + 0.587 * g + 0.114 * b
lenna_rgb[:, :, 0] = gray
lenna_rgb[:, :, 1] = gray
lenna_rgb[:, :, 2] = gray

lenna_rgb[len_cor_res > 0.1] = (0, 255, 0)

cv2.imshow('lenna corner', lenna_rgb)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('./result/part_3_corner_bin_lenna.png', lenna_rgb)

# shapes.png
shapes_rgb = cv2.imread('shapes.png', cv2.IMREAD_COLOR)

b, g, r = shapes_rgb[:, :, 0], shapes_rgb[:, :, 1], shapes_rgb[:, :, 2]
gray = 0.299 * r + 0.587 * g + 0.114 * b
shapes_rgb[:, :, 0] = gray
shapes_rgb[:, :, 1] = gray
shapes_rgb[:, :, 2] = gray
shapes_rgb[shp_cor_res > 0.1] = (0, 255, 0)

cv2.imshow('shapes corner', shapes_rgb)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('./result/part_3_corner_bin_shapes.png', shapes_rgb)

## (c)
def non_maximum_suppression_win(R, win_size = 11):
    pad_size = win_size // 2
    h, w = R.shape

    pad_hor = np.zeros((h, pad_size))
    R_pad = np.concatenate((pad_hor, R, pad_hor), axis=1)
    pad_ver = np.zeros((5, w + 2 * pad_size))
    R_pad = np.concatenate((pad_ver, R_pad, pad_ver), axis=0)

    local_max_R = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            local_max_R[i, j] = np.max(R_pad[i: i + win_size, j: j + win_size].flatten())

    suppressed_R = R.copy()
    suppressed_R[R <= 0.1] = 0
    suppressed_R[R < local_max_R] = 0

    return suppressed_R

## (d)
# lenna.png
tic = time.time()
len_sup_res = non_maximum_suppression_win(len_cor_res, 11)
tac = time.time()
print(f'lenna NMS corner computation time : {tac - tic}')

sup_y, sup_x = np.where(len_sup_res != 0)
lenna_nms = cv2.imread('lenna.png', cv2.IMREAD_COLOR)

b, g, r = lenna_nms[:, :, 0], lenna_nms[:, :, 1], lenna_nms[:, :, 2]
gray = 0.299 * r + 0.587 * g + 0.114 * b
lenna_nms[:, :, 0] = gray
lenna_nms[:, :, 1] = gray
lenna_nms[:, :, 2] = gray

for i in range(len(sup_x)):
    cv2.circle(lenna_nms, (sup_x[i], sup_y[i]), 7, (0, 255, 0), 2)

cv2.imshow('lenna NMS corner', lenna_nms)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('./result/part_3_corner_sup_lenna.png', lenna_nms)

# shapes.png
tic = time.time()
shp_sup_res = non_maximum_suppression_win(shp_cor_res, 11)
tac = time.time()
print(f'shapes NMS corner computation time : {tac - tic}')

sup_y, sup_x = np.where(shp_sup_res != 0)
shapes_nms = cv2.imread('shapes.png', cv2.IMREAD_COLOR)

b, g, r = shapes_nms[:, :, 0], shapes_nms[:, :, 1], shapes_nms[:, :, 2]
gray = 0.299 * r + 0.587 * g + 0.114 * b
shapes_nms[:, :, 0] = gray
shapes_nms[:, :, 1] = gray
shapes_nms[:, :, 2] = gray

for i in range(len(sup_x)):
    cv2.circle(shapes_nms, (sup_x[i], sup_y[i]), 7, (0, 255, 0), 2)

cv2.imshow('shapes NMS corner', shapes_nms)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('./result/part_3_corner_sup_shapes.png', shapes_nms)
