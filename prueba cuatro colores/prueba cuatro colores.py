#Algoritmo de deteccion de colores
#Por Glar3
#
#
#Detecta objetos verdes, elimina el ruido y busca su centro
 
import cv2
import numpy as np
 
#Iniciamos la camara
captura = cv2.VideoCapture(0)
 
while(1):
     
    #Capturamos una imagen y la convertimos de RGB -> HSV
    _, imagen = captura.read()
    imagen = cv2.blur(imagen,(3,3))
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
 
    #Establecemos el rango de colores que vamos a detectar
    verde_bajos = np.array([49,50,50], dtype=np.uint8)
    verde_altos = np.array([80, 255, 255], dtype=np.uint8)

    rojo_bajos = np.array([172,50,50], dtype=np.uint8)
    rojo_altos = np.array([180, 255, 255], dtype=np.uint8)

    azul_bajos = np.array([99,50,50], dtype=np.uint8)
    azul_altos = np.array([128, 255, 255], dtype=np.uint8)

    amarillo_bajos = np.array([23,50,50], dtype=np.uint8)
    amarillo_altos = np.array([33, 255, 255], dtype=np.uint8)
 
    #Crear una mascara con solo los pixeles dentro del rango de verdes y azules
    mask_azul = cv2.inRange(hsv, azul_bajos, azul_altos)
    mask_verde = cv2.inRange(hsv, verde_bajos, verde_altos)
    mask_amarillo = cv2.inRange(hsv, amarillo_bajos, amarillo_altos)
    mask_rojo = cv2.inRange(hsv, rojo_bajos, rojo_altos)

    mask = mask_verde + mask_azul + mask_rojo + mask_amarillo

    res = cv2.bitwise_and(imagen, imagen, mask= mask)
    '''
    #Encontrar el area de los objetos que detecta la camara
    moments = cv2.moments(mask)
    area = moments['m00']
 
    #Descomentar para ver el area por pantalla
    #print area
    if(area > 2000000):
         
        #Buscamos el centro x, y del objeto
        x = int(moments['m10']/moments['m00'])
        y = int(moments['m01']/moments['m00'])
         
        #Mostramos sus coordenadas por pantalla
        #print "x = ", x
        #print "y = ", y
 
        #Dibujamos una marca en el centro del objeto
        cv2.rectangle(imagen, (x, y), (x+2, y+2),(0,0,255), 2)
        '''
     
    #Mostramos la imagen original con la marca del centro y
    #la mascara
    #cv2.imshow('mask', mask)
    cv2.imshow('res', res)
    cv2.imshow('Camara', imagen)
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break
 
cv2.destroyAllWindows()
