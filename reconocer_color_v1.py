#reconocer color v1.0
#print 18
import cv2, numpy as np

#Variables Globales

rojo = 1
azul = 2
amarillo = 3
verde = 4

boundaries = [([17, 15, 100], [50, 56, 200]),
              ([86, 31, 4], [220, 88, 50]),
              ([25, 146, 190], [62, 174, 250]),
              ([103, 86, 65], [145, 133, 128])]

captura = cv2.VideoCapture(0)

'''while(True):
    imagen = captura.read()
    #hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
    for (lower, upper) in boundaries:
	# create NumPy arrays from the boundaries
	lower = np.array(lower, dtype = "uint8")
	upper = np.array(upper, dtype = "uint8")
 
	# find the colors within the specified boundaries and apply
	# the mask
	mask = cv2.inRange(image, lower, upper)
	output = cv2.bitwise_and(image, image, mask = mask)
 
	# show the images
	cv2.imshow("images", np.hstack([image, output]))
	cv2.waitKey(0)'''

imagen = captura.read()
#hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
for (lower, upper) in boundaries:
    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype = np.uint8)
    upper = np.array(upper, dtype = np.uint8)
 
    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(imagen, lower, upper)
    output = cv2.bitwise_and(imagen, imagen, mask = mask)
 
    # show the images
    cv2.imshow("images", np.hstack([image, output]))
    cv2.waitKey(0)
