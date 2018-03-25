 
import cv2, sys, os
import numpy as np

colores = {verde : (np.array([49,50,50], dtype=np.uint8), np.array([80, 255, 255], dtype=np.uint8)),
           rojo : (np.array([172,50,50], dtype=np.uint8), np.array([180, 255, 255], dtype=np.uint8)),
           azul : (np.array([99,50,50], dtype=np.uint8), np.array([128, 255, 255], dtype=np.uint8)),
           amarillo : (np.array([23,50,50], dtype=np.uint8), np.array([33, 255, 255], dtype=np.uint8))}

#Definimos las funciones
#Reinicia el shell para apagar la comunicacion con la camara
def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def mask(hsv, (bajos, altos)):
    return cv2.inRange(hsv, bajos, altos)

#Iniciamos la camara
captura = cv2.VideoCapture(0)
 
while(1):
     
    #Capturamos una imagen y la convertimos de RGB -> HSV
    _,imagen = captura.read()
    imagen = cv2.blur(imagen,(3,3))
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

'''    #Establecemos el rango de colores que vamos a detectar
    #funcion y diccionario
    verde_bajos = np.array([49,50,50], dtype=np.uint8)
    verde_altos = np.array([80, 255, 255], dtype=np.uint8)

    rojo_bajos = np.array([172,50,50], dtype=np.uint8)
    rojo_altos = np.array([180, 255, 255], dtype=np.uint8)

    azul_bajos = np.array([99,50,50], dtype=np.uint8)
    azul_altos = np.array([128, 255, 255], dtype=np.uint8)

    amarillo_bajos = np.array([23,50,50], dtype=np.uint8)
    amarillo_altos = np.array([33, 255, 255], dtype=np.uint8)'''

    #Crear una mascara con solo los pixeles dentro del rango de los colores
    #funcion
    mask_azul = cv2.inRange(hsv, colores[azul])
    mask_verde = cv2.inRange(hsv, colores[verde])
    mask_amarillo = cv2.inRange(hsv, colores[amarillo])
    mask_rojo = cv2.inRange(hsv, colores[rojo])

    #Eliminamos el ruido del rojo
    #funcion
    kernel = np.ones((3, 3), np.uint8)

    noise_rojo = cv2.erode(mask_rojo, kernel, iterations = 1)
    noise_rojo = cv2.morphologyEx(noise_rojo, cv2.MORPH_OPEN, kernel)
    noise_rojo = cv2.dilate(noise_rojo, kernel, iterations = 1)

    #mask = mask_verde + mask_azul + mask_rojo + mask_amarillo
    mask = noise_rojo

    #Muestra la mascara solo con los colores seleccionados
    color = cv2.bitwise_and(imagen, imagen, mask= mask)
    '''
    #Encontrar el area de los objetos que detecta la camara
    moments = cv2.moments(mask)
    area = moments['m00']
 
    #Descomentar para ver el area por pantalla
    #print area
    if(area > 1000000):
         
        #Buscamos el centro x, y del objeto
        x = int(moments['m10']/moments['m00'])
        y = int(moments['m01']/moments['m00'])
         
        #Mostramos sus coordenadas por pantalla
        #print "x = ", x
        #print "y = ", y
 
        #Dibujamos una marca en el centro del objeto
        cv2.rectangle(imagen, (x, y), (x+2, y+2),(255,255,255), 2)
        '''
     
    #Mostramos la imagen original con la marca del centro y
    #la mascara
    cv2.imshow('mask', mask_rojo)
    cv2.imshow('noise', mask)
    #cv2.imshow('Color', mask)
    #cv2.imshow('Camara', imagen)

    #Termina con la tecla ESC
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break
 
cv2.destroyAllWindows()
restart()
