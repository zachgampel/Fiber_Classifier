import cv2
import numpy as np


def modifyVisiblePoints(visiblePoints):
    remainingPoints = []
    for point in visiblePoints:
        count = 0
        for adjacentPoint in visiblePoints:
            if np.abs(adjacentPoint[0] - point[0]) == 1 and np.abs(adjacentPoint[1] - point[1]) == 1:
                count = count + 1
        if count >= 2:
            remainingPoints.append(point)
    return remainingPoints


# downsize, blur, then resize the mask to push out the edges a bit
def blurMask(img, mask):
    mask = cv2.resize(mask, dsize=(mask.shape[0] // 3, mask.shape[1] // 3), interpolation=cv2.INTER_AREA)
    mask = cv2.GaussianBlur(mask, (9, 9), 0)
    mask = cv2.resize(mask, dsize=(img.shape[1], img.shape[0]), interpolation=cv2.INTER_AREA)

    mask = cv2.bitwise_not(mask)
    mask = cv2.resize(mask, dsize=(mask.shape[0] // 3, mask.shape[1] // 3), interpolation=cv2.INTER_AREA)
    mask = cv2.GaussianBlur(mask, (9, 9), 0)
    mask = cv2.resize(mask, dsize=(img.shape[1], img.shape[0]), interpolation=cv2.INTER_AREA)
    mask = cv2.bitwise_not(mask)

    x, y = img.shape
    for i in range(x):
        for j in range(y):
            if mask[i][j] < 150:
                mask[i][j] = 0
            else:
                mask[i][j] = 255
    return mask

def getForegroundMask(img, square_length=20, cutoff_roughness=1):
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    x, y = img.shape

    mask = np.zeros(img.shape, np.uint8)

    # find roughness of each sector of the rough image, and if it's rough enough make it visible in the mask
    visible_points = []
    for i in range(0, x // square_length):
        for j in range(0, y // square_length):
            roughness = np.mean(
                img[i * square_length:(i + 1) * square_length, j * square_length:(j + 1) * square_length])
            if roughness > cutoff_roughness:
                visible_points.append([i, j])

    visible_points = modifyVisiblePoints(visible_points)

    for point in visible_points:
        mask[point[0] * square_length:(point[0] + 1) * square_length, point[1] * square_length:(point[1] + 1) * square_length] = 255

    mask = blurMask(img, mask)

    # set all nonzero values in mask to max value = 255
    for i in range(x):
        for j in range(y):
            if mask[i][j] > 0:
                mask[i][j] = 255

    return mask


