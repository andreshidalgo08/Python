import cv2, numpy as np

captura = cv2.VideoCapture(0)

imagen = captura.read()

lower = np.array([17, 15, 100], dtype = "uint8")
upper = np.array([50, 56, 200], dtype = "uint8")

mask = cv2.inRange(imagen, lower, upper)
output = cv2.bitwise_and(imagen, imagen, mask = mask)

cv2.imshow("images", np.hstack([image, output]))
cv2.waitKey(0)
