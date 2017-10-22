import cv2
import numpy as np
from shape_recognition.utils import order_points


def gray_blur_gaussian(image, kernel_size=(5, 5), kernel_deviation=0):
    """
    Convert to grayscale and Blur it using a Gaussian filter
    to reduce noise as well as reducing detail"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, kernel_size, kernel_deviation)
    return gray


def find_contours(image, cannyMin=100, cannyMax=200):
    """Detect edges using a canny edge detector algoritgh
    http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_canny/py_canny.html
    """
    edged = cv2.Canny(image, cannyMin, cannyMax)
    # Find contours in an image
    # http://docs.opencv.org/3.1.0/d4/d73/tutorial_py_contours_begin.html
    im2, contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    return contours, hierarchy, edged


def find_contour_edges(c, epsilon=0.02):
    """Find the edges of the contour"""
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, epsilon * peri, True)
    return approx


def find_frame(contours):
    """ Find the largest rectangular contout - probably the frame of the im"""
    # Sort the contours by area and use the largest ones only
    cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

    # loop over the contours and find the ones that are rectangles
    # Approximate them and find out wjether they have 4 edges
    # http://docs.opencv.org/trunk/dd/d49/tutorial_py_contour_features.html
    for c in cnts:
        # approximate the contour
        approx = find_contour_edges(c)

        # if our approximated contour has four points, then we
        # can assume that we have found our screen
        if len(approx) == 4:
            frame = approx
            break
    return frame


def transform_to_frame(image, frame, newImageW, newImageH, crop=None):
    """Transform image to a birds eye view given the frame location"""
    pts1 = order_points(frame)
    pts2 = np.float32([[0, 0], [newImageW, 0], [newImageW, newImageH], [0, newImageH]])

    # Get transformation matrix
    M = cv2.getPerspectiveTransform(pts1, pts2)
    topDownImage = cv2.warpPerspective(image, M, (newImageW, newImageH))

    if (crop is not None):
        if (crop < 1):
            raise ValueError("Crop must be more than 0 or None")
        topDownImage = topDownImage[crop:-crop, crop:-crop]
        topDownImage = cv2.copyMakeBorder(topDownImage, crop, crop, crop, crop, cv2.BORDER_REPLICATE)

    return topDownImage


imageNameRoot = "images/image1"
imageName = imageNameRoot + ".jpeg"
image = cv2.imread(imageName)

gray = gray_blur_gaussian(image)
cv2.imwrite(imageNameRoot + "-1blurred.jpg", gray)

contours, h, edged = find_contours(gray)
cv2.imwrite(imageNameRoot + "-2edged.jpg", edged)

imageFrame = find_frame(contours)
topDownImage = transform_to_frame(image, imageFrame, 1000, 1000, 10)
grayTopDown = gray_blur_gaussian(topDownImage)
cv2.imwrite(imageNameRoot + "-3topdown.jpg", grayTopDown)

contours, h, e = find_contours(grayTopDown)
cv2.imwrite(imageNameRoot + "-4dged.jpg", e)

# Find the outer edge
cnt = sorted(contours, key=cv2.contourArea, reverse=True)[0]
approx = find_contour_edges(cnt)
cv2.drawContours(topDownImage, [approx], 0, (0, 255, 0), 2)
cv2.imwrite(imageNameRoot + "-5contour.jpg", topDownImage)

print(len(contours), grayTopDown.shape)
print(approx)
