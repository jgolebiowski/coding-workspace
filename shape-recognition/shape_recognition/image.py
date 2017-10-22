import cv2
import numpy as np
import os
from .utils import order_points

"""The image class"""


class Image(object):
    """This is the main image object, read in, operate and print the photos"""

    def __init__(self, imagePath):
        abs_path = os.path.abspath(imagePath)
        self.image_root_path, full_image_name = os.path.split(abs_path)
        self.image_name, self.image_extension = os.path.splitext(full_image_name)
        self._original_image = cv2.imread(abs_path)
        self.image = cv2.imread(abs_path)

        # - counter for dumping images
        self.image_dumps = 0

    def reset(self):
        """Reset the image back ot the original"""
        self.image = self._original_image
        self.contours = None

    def write_image(self, extra_string=""):
        """Dump the image"""
        name = self.image_root_path + "/" + self.image_name
        name += extra_string + str(self.image_dumps) + self.image_extension
        cv2.imwrite(name, self.image)
        self.image_dumps += 1

    def gray_blur_gaussian(self, kernel_size=(5, 5), kernel_deviation=0):
        """Convert to grayscale and Blur it using a Gaussian filter
        to reduce noise as well as reducing detail"""
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image = cv2.GaussianBlur(self.image, kernel_size, kernel_deviation)
        return self.image

    def find_contours(self, cannyMin=100, cannyMax=200):
        """Detect edges using a canny edge detector algoritgh
        http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_canny/py_canny.html
        """
        self.image = cv2.Canny(self.image, cannyMin, cannyMax)
        # Find contours in an image
        # http://docs.opencv.org/3.1.0/d4/d73/tutorial_py_contours_begin.html
        im2, self.contours, hierarchy = cv2.findContours(self.image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        return self.contours, hierarchy, self.image

    def find_contour_edges(self, c, epsilon=0.02):
        """Find the edges of the contour"""
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon * peri, True)
        return approx

    def frame_image(self, newImageW, newImageH, crop, **kwargs):
        """Detect the frame and transform the image to it"""
        self.find_contours(**kwargs)
        frame = self.find_frame()
        self.transform_to_frame(frame, newImageW, newImageH, crop)
        return self.image

    def transform_to_frame(self, frame, newImageW, newImageH, crop=None):
        """Transform image to a birds eye view given the frame location"""
        pts1 = order_points(frame)
        pts2 = np.float32([[0, 0], [newImageW, 0], [newImageW, newImageH], [0, newImageH]])

        # Get transformation matrix
        M = cv2.getPerspectiveTransform(pts1, pts2)
        self.image = cv2.warpPerspective(self.image, M, (newImageW, newImageH))

        if (crop is not None):
            if (crop < 1):
                raise ValueError("Crop must be more than 0 or None")
            self.image = self.image[crop:-crop, crop:-crop]
            self.image = cv2.copyMakeBorder(self.image, crop, crop, crop, crop, cv2.BORDER_REPLICATE)

        return self.image

    def find_frame(self, contours=None):
        """ Find the largest rectangular contout - probably the frame of the im"""
        # Sort the contours by area and use the largest ones only
        if contours is None:
            contours = self.contours
        cnts = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

        # loop over the contours and find the ones that are rectangles
        # Approximate them and find out wjether they have 4 edges
        # http://docs.opencv.org/trunk/dd/d49/tutorial_py_contour_features.html
        for c in cnts:
            # approximate the contour
            approx = self.find_contour_edges(c)

            # if our approximated contour has four points, then we
            # can assume that we have found our screen
            if len(approx) == 4:
                frame = approx
                break
        return frame

    def find_largest_contour(self):
        """Find the largest contour"""
        contours, h, e = self.find_contours()
        cnt = sorted(contours, key=cv2.contourArea, reverse=True)[0]
        approx = self.find_contour_edges(cnt)
        return approx
