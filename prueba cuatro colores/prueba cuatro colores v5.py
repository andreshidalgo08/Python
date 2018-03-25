#v5
#Se le agrega deteccion de contorno y centro

import cv2, sys, os
import numpy as np

#Falta jugar con los colores
colores = {'verde' : (np.array([49,0,0], dtype=np.uint8), np.array([80, 255, 255], dtype=np.uint8)),
           'rojo' : (np.array([172,50,50], dtype=np.uint8), np.array([180, 255, 255], dtype=np.uint8)),
           'azul' : (np.array([99,50,50], dtype=np.uint8), np.array([120, 255, 255], dtype=np.uint8)),
           'amarillo' : (np.array([23,50,50], dtype=np.uint8), np.array([33, 255, 255], dtype=np.uint8))}

kernel = np.ones((3, 3), np.uint8)

frames = 0

#Definimos las funciones
#Reinicia el shell para apagar la comunicacion con la camara
def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)

#Elimina el ruido para un color
def noise(mask):
    noise = cv2.erode(mask, kernel, iterations = 1)
    noise = cv2.morphologyEx(noise, cv2.MORPH_OPEN, kernel)
    noise = cv2.dilate(noise, kernel, iterations = 1)
    return noise

#Dibuja el contorn y el centro del objeto con mayor area
def contorno(mask):
    im2, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        #Escogemos el controno con mayor area
        max_area = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area = area
                best_cnt = cnt
                
        cv2.drawContours(imagen, [best_cnt], 0, (0,255,0), 3)
        #Encontramos el centro
        M = cv2.moments(best_cnt)
        x,y = int(M['m10']/M['m00']), int(M['m01']/M['m00'])

        #Dibujamos una marca en el centro del objeto
        cv2.rectangle(imagen, (x, y), (x+2, y+2),(255,255,255), 2)

#Iniciamos la camara
captura = cv2.VideoCapture(0)

while(1):
    if frames < 2:
        frames = frames + 1

    #Capturamos una imagen y la convertimos de RGB -> HSV
    _,imagen = captura.read()
    imagen = cv2.blur(imagen,(3,3))
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    #Crear una mascara con solo los pixeles dentro del rango de los colores
    mask_azul = cv2.inRange(hsv, colores['azul'][0], colores['azul'][1])
    mask_rojo = cv2.inRange(hsv, colores['rojo'][0], colores['rojo'][1])
    mask_verde = cv2.inRange(hsv, colores['verde'][0], colores['verde'][1])
    mask_amarillo = cv2.inRange(hsv, colores['amarillo'][0], colores['amarillo'][1])

    #Eliminamos el ruido
    noise_azul = noise(mask_azul)
    noise_rojo = noise(mask_rojo)
    noise_verde = noise(mask_verde)
    noise_amarillo = noise(mask_amarillo)

    #Marcamos el contorno
    if frames == 2:
        contorno(noise_azul)
        contorno(noise_rojo)
        contorno(noise_verde)
        contorno(noise_amarillo)

    #Mascara con todos los colores
    mask = noise_azul + noise_rojo + noise_verde + noise_amarillo

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
restart()
