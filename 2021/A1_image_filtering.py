import cv2
import numpy as np

lenna_img = cv2.imread('lenna.png', cv2.IMREAD_GRAYSCALE)
shapes_img = cv2.imread('shapes.png', cv2.IMREAD_GRAYSCALE)

# 1-1
## (a)
def cross_correlation_1d(img, kernel):
    horizontal = True if len(kernel.shape) == 1 else False
    kernel_size = kernel.shape[0]
    pad_size = (kernel_size - 1) // 2

    if not horizontal:
        img = img.T
        kernel = kernel.T

    img = img.astype(np.float64)
    img_h, img_w = img.shape
    pad_img = img.copy()

    # making padded image
    pad_l = np.reshape(img[:, 0], (-1, 1))
    pad_r = np.reshape(img[:, -1], (-1, 1))

    for _ in range(pad_size):
        pad_img = np.concatenate((pad_l, pad_img, pad_r), axis=1)

    # cross_correlation
    filtered_img = np.zeros_like(img).astype(np.float64)

    pixel_val = 0
    for x in range(img_h):
        for y in range(img_w):
            pixel_val = np.sum(pad_img[x, y: y + kernel_size] * kernel)
            filtered_img[x, y] = pixel_val
            pixel_val = 0

    if not horizontal:
        filtered_img = filtered_img.T

    return filtered_img


def cross_correlation_2d(img, kernel):
    kernel_h, kernel_w = kernel.shape
    pad_h = (kernel_h - 1) // 2
    pad_w = (kernel_w - 1) // 2

    img = img.astype(np.float64)
    img_h, img_w = img.shape
    pad_img = img.copy()

    # making padded image
    pad_l = np.reshape(img[:, 0], (-1, 1))
    pad_r = np.reshape(img[:, -1], (-1, 1))

    for _ in range(pad_w):
        pad_img = np.concatenate((pad_l, pad_img, pad_r), axis=1)

    pad_u = np.reshape(pad_img[0, :], (1, -1))
    pad_d = np.reshape(pad_img[-1, :], (1, -1))

    for _ in range(pad_h):
        pad_img = np.concatenate((pad_u, pad_img, pad_d), axis=0)

    # cross_correlation
    filtered_img = np.zeros_like(img).astype(np.float64)

    pixel_val = 0
    for x in range(img_h):
        for y in range(img_w):
            pixel_val = np.sum(pad_img[x:x + kernel_h, y: y + kernel_w] * kernel)
            filtered_img[x, y] = pixel_val
            pixel_val = 0

    return filtered_img


# 1-2
## (a)
def get_gaussian_filter_1d(size, sigma):
    gaussian_filter = np.arange(1, size + 1, 1).astype(np.float64)

    center = (size + 1) // 2
    gaussian_filter -= center

    gaussian_filter **= 2

    gaussian_filter *= (-1 / (2 * sigma ** 2))

    gaussian_filter = np.exp(gaussian_filter)

    gaussian_filter /= (np.sqrt(2 * np.pi) * sigma)

    gaussian_filter /= np.sum(gaussian_filter)

    return gaussian_filter


def get_gaussian_filter_2d(size, sigma):
    # float64
    gaussian_filter = np.zeros((size, size))

    center = size // 2
    for i in range(size):
        for j in range(size):
            gaussian_filter[i, j] = (i - center) ** 2 + (j - center) ** 2

    gaussian_filter *= (-1 / (2 * sigma ** 2))
    gaussian_filter = np.exp(gaussian_filter)

    gaussian_filter /= (2 * np.pi * sigma ** 2)

    gaussian_filter /= np.sum(gaussian_filter.flatten())

    return gaussian_filter

## (c)
if __name__ == '__main__':
    print(f'gaussian 1d : {get_gaussian_filter_1d(5, 1)}')
    print(f'gaussian 2d : {get_gaussian_filter_2d(5, 1)}')

    ## (d)
    size_list = [5, 11, 17]
    sigma_list = [1, 6, 11]

    results = None
    for size in size_list:
        filter_img = None
        for sigma in sigma_list:
            gauss_filter = get_gaussian_filter_2d(size, sigma)
            filter_img_i = cross_correlation_2d(lenna_img, gauss_filter)
            cv2.putText(filter_img_i, f'{size}x{size} s {sigma}', (30, 30), 3, 1, (255, 255, 255), 2)
            if sigma == sigma_list[0]:
                filter_img = filter_img_i
            else:
                filter_img = np.concatenate((filter_img, filter_img_i), axis=1)

        if size == size_list[0]:
            results = filter_img
        else:
            results = np.concatenate((results, filter_img), axis=0)

    cv2.imshow('lenna results', results)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite('./result/part_1_gaussian_filtered_lenna.png', results)


    results = None
    size_list = [3, 5, 7]
    sigma_list = [1, 5, 10]

    for size in size_list:
        filter_img = None
        for sigma in sigma_list:
            gauss_filter = get_gaussian_filter_2d(size, sigma)
            filter_img_i = cross_correlation_2d(shapes_img, gauss_filter)
            cv2.putText(filter_img_i, f'{size}x{size} s {sigma}', (30, 30), 3, 1, (0, 0, 0), 2)
            if sigma == sigma_list[0]:
                filter_img = filter_img_i
            else:
                filter_img = np.concatenate((filter_img, filter_img_i), axis=1)

        if size == size_list[0]:
            results = filter_img
        else:
            results = np.concatenate((results, filter_img), axis=0)

    cv2.imshow('shapes results', results)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite('./result/part_1_gaussian_filtered_shapes.png', results)

    ## (e)
    import time

    tic1 = time.time()
    filter_2d = get_gaussian_filter_2d(17, 6)
    lenna_2d = cross_correlation_2d(lenna_img, filter_2d)
    tac1 = time.time()

    tic2 = time.time()
    filter_1d = get_gaussian_filter_1d(17, 6)
    lenna_1d = cross_correlation_1d(lenna_img, filter_1d)
    lenna_1d = cross_correlation_1d(lenna_1d.T, filter_1d)
    lenna_1d = lenna_1d.T
    tac2 = time.time()

    print(f'2D time : {tac1-tic1}, 1D time : {tac2-tic2}')

    lenna_diff = lenna_2d - lenna_1d
    print(f'lenna difference : {np.sum(np.abs(lenna_diff))}')


    tic1 = time.time()
    filter_2d = get_gaussian_filter_2d(17, 6)
    shapes_2d = cross_correlation_2d(shapes_img, filter_2d)
    tac1 = time.time()

    tic2 = time.time()
    filter_1d = get_gaussian_filter_1d(17, 6)
    shapes_1d = cross_correlation_1d(shapes_img, filter_1d)
    shapes_1d = cross_correlation_1d(shapes_1d.T, filter_1d)
    shapes_1d = shapes_1d.T
    tac2 = time.time()

    print(f'2D time : {tac1-tic1}, 1D time : {tac2-tic2}')

    shapes_diff = shapes_2d - shapes_1d
    print(f'shapes difference : {np.sum(np.abs(shapes_diff))}')

