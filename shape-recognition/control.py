import cv2
import numpy as np
from shape_recognition.image import Image


image = Image("images/image1.jpeg")
image.gray_blur_gaussian()
image.write_image("blured")
image.find_contours()
image.write_image("edged")

frame = image.find_frame()
image.reset()
image.transform_to_frame(frame, 1000, 1000, 10)
image.gray_blur_gaussian()
image.write_image("topdown")

approx = image.find_largest_contour()

image.reset()
image.transform_to_frame(frame, 1000, 1000, 10)
cv2.drawContours(image.image, [approx], 0, (0, 255, 0), 2)
image.write_image("contour")

print(approx)
