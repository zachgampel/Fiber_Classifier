import cv2
import numpy as np
from matplotlib import pyplot as plt
from Utils import imshow


# Smooths by averaging; doesn't work great
def imageAverager(img, kernel_size):
    kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size * kernel_size)
    return cv2.filter2D(img, -1, kernel)


def gaussianBlur(img, size):
    return cv2.GaussianBlur(img, (size, size), 0)


def mediumBlur(img, size):
    return cv2.medianBlur(img, size)


img = cv2.imread('fiber2.png', 0)
ret, thresh1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
imshow(thresh1)
img = cv2.imread('fiber.png', 0)
ret, thresh1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
imshow(thresh1)
img = cv2.imread('fiber.png', 0)
ret, thresh1 = cv2.threshold(img, 127, 255, cv2.THRESH_TRUNC)
imshow(thresh1)
img = cv2.imread('fiber.png', 0)
ret, thresh1 = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO)
imshow(thresh1)
img = cv2.imread('fiber.png', 0)
ret, thresh1 = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO_INV)
imshow(thresh1)

# global thresholding
ret1, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

# Otsu's thresholding
ret2, th2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Otsu's thresholding after Gaussian filtering
blur = cv2.GaussianBlur(img, (5, 5), 0)
ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# plot all the images and their histograms
images = [img, 0, th1,
          img, 0, th2,
          blur, 0, th3]
titles = ['Original Noisy Image', 'Histogram', 'Global Thresholding (v=127)',
          'Original Noisy Image', 'Histogram', "Otsu's Thresholding",
          'Gaussian filtered Image', 'Histogram', "Otsu's Thresholding"]

for i in range(3):
    plt.subplot(3, 3, i * 3 + 1), plt.imshow(images[i * 3], 'gray')
    plt.title(titles[i * 3]), plt.xticks([]), plt.yticks([])
    plt.subplot(3, 3, i * 3 + 2), plt.hist(images[i * 3].ravel(), 256)
    plt.title(titles[i * 3 + 1]), plt.xticks([]), plt.yticks([])
    plt.subplot(3, 3, i * 3 + 3), plt.imshow(images[i * 3 + 2], 'gray')
    plt.title(titles[i * 3 + 2]), plt.xticks([]), plt.yticks([])
plt.show()
