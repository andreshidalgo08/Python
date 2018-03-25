import cv2, sys, os
import numpy as np

#Falta jugar con los colores
colores = {'verde' : (np.array([49,0,0], dtype=np.uint8), np.array([80, 255, 255], dtype=np.uint8)),
           'rojo' : (np.array([172,50,50], dtype=np.uint8), np.array([180, 255, 255], dtype=np.uint8)),
           'azul' : (np.array([99,50,50], dtype=np.uint8), np.array([120, 255, 255], dtype=np.uint8)),
           'amarillo' : (np.array([23,50,50], dtype=np.uint8), np.array([33, 255, 255], dtype=np.uint8))}

kernel = np.ones((3, 3), np.uint8)

#Elimina el ruido para un color
def noise(mask):
    noise = cv2.erode(mask, kernel, iterations = 1)
    noise = cv2.morphologyEx(noise, cv2.MORPH_OPEN, kernel)
    noise = cv2.dilate(noise, kernel, iterations = 1)
    return noise

frames = 0

#Iniciamos la camara
captura = cv2.VideoCapture(0)

while(1):

    frames = frames + 1
    
    #Capturamos una imagen y la convertimos de RGB -> HSV
    _,imagen = captura.read()
    imagen = cv2.blur(imagen,(3,3))
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    #Crear una mascara con solo los pixeles dentro del rango de los colores
    mask = cv2.inRange(hsv, colores['rojo'][0], colores['rojo'][1])
    
    #Eliminamos el ruido
    #noise = noise(mask)

    if frames > 2:
        im2, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        max_area = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area = area
                best_cnt = cnt
            
        cv2.drawContours(imagen, [best_cnt], 0, (0,255,0), 3)
        M = cv2.moments(best_cnt)
        x,y = int(M['m10']/M['m00']), int(M['m01']/M['m00'])

        #Dibujamos una marca en el centro del objeto
        cv2.rectangle(imagen, (x, y), (x+2, y+2),(255,255,255), 2)

    #Mascara con todos los colores
    #mask = noise

    #Imagen con solo los colores
    color = cv2.bitwise_and(imagen, imagen, mask= mask)

    #Mostramos las imagenes
    cv2.imshow('Filtrado', color)
    cv2.imshow('Camara', imagen)

    #Termina con la tecla ESC
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break

cv2.destroyAllWindows()

