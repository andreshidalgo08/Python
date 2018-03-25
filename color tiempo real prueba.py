import cv2
import numpy as np
 
cap = cv2.VideoCapture(0)
 
def nothing(x):
    pass
 
#Creamos una ventana llamada 'image' en la que habra todos los sliders
cv2.namedWindow('image')
cv2.createTrackbar('H min','image',0,180,nothing)
cv2.createTrackbar('H max','image',0,180,nothing)
cv2.createTrackbar('S min','image',0,255,nothing)
cv2.createTrackbar('S max','image',0,255,nothing)
cv2.createTrackbar('V min','image',0,255,nothing)
cv2.createTrackbar('V max','image',0,255,nothing)
 
while(1):
  _,frame = cap.read() #Leer un frame
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Convertirlo a espacio de color HSV
 
  #Los valores maximo y minimo de H,S y V se guardan en funcion de la posicion de los sliders
  hMin = cv2.getTrackbarPos('H min','image')
  hMax = cv2.getTrackbarPos('H max','image')
  sMin = cv2.getTrackbarPos('S min','image')
  sMax = cv2.getTrackbarPos('S max','image')
  vMin = cv2.getTrackbarPos('V min','image')
  vMax = cv2.getTrackbarPos('V max','image')
 
  #Se crea un array con las posiciones minimas y maximas
  lower=np.array([hMin,sMin,vMin])
  upper=np.array([hMax,sMax,vMax])
 
  #Deteccion de colores
  mask = cv2.inRange(hsv, lower, upper)

  #Imagen con solo los colores
  color = cv2.bitwise_and(frame, frame, mask= mask)
  
  #Mostrar los resultados y salir
  cv2.imshow('camara',frame)
  cv2.imshow('mask',color)
  k = cv2.waitKey(5) & 0xFF
  if k == 27:
    break
cv2.destroyAllWindows()
