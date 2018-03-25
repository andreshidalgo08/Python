#v5
#Se le agrega deteccion de contorno

import cv2, sys, os
import numpy as np

#Falta jugar con los colores
colores = {'verde' : (np.array([49,0,0], dtype=np.uint8), np.array([80, 255, 255], dtype=np.uint8)),
           'rojo' : (np.array([172,50,50], dtype=np.uint8), np.array([180, 255, 255], dtype=np.uint8)),
           'azul' : (np.array([99,50,50], dtype=np.uint8), np.array([120, 255, 255], dtype=np.uint8)),
           'amarillo' : (np.array([23,50,50], dtype=np.uint8), np.array([33, 255, 255], dtype=np.uint8))}

kernel = np.ones((3, 3), np.uint8)

num_frames = 0

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

#Iniciamos la camara
captura = cv2.VideoCapture(0)

while(1):

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
