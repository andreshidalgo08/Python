#v7
#Se le agrega manejo de hilos

import cv2, sys, os, math
import numpy as np

colores = []

kernel = np.ones((3, 3), np.uint8)

HSV = True
ON = False

def nothing(x):
    pass

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

#Dibuja el contorno y el centro del objeto con mayor area
def contorno(mask):
    global imagen
    _, contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        #Escogemos el controno con mayor area
        max_area = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area = area
                best_cnt = cnt
        '''
        cv2.drawContours(imagen, [best_cnt], 0, (255,255,255), 2)
        #Encontramos el centro
        M = cv2.moments(best_cnt)
        x,y = int(M['m10']/M['m00']), int(M['m01']/M['m00'])

        #Dibujamos una marca en el centro del objeto
        cv2.rectangle(imagen, (x, y), (x+2, y+2),(255,255,255), 2)
        '''
        #Minimo circulo
        (x,y),radius = cv2.minEnclosingCircle(best_cnt)
        centro = (int(x),int(y))
        radio = int(radius)
        #print radio
        #radio = 45
        imagen = cv2.circle(imagen,centro,radio,(255, 255, 255),2)
        
        #Dibujamos una marca en el centro del objeto
        cv2.rectangle(imagen, centro, (centro[0] + 2, centro[1] + 2),(255,255,255), 2)
        
def distancia(p,q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

#Iniciamos la camara
captura = cv2.VideoCapture(0)

while(1):

    #Capturamos una imagen y la convertimos de RGB -> HSV
    _,imagen = captura.read()
    #imagen = cv2.blur(imagen,(3,3))
    #Se le aplican diferentes filtros
    imagen = cv2.bilateralFilter(imagen,5,75,75) #5 o 9, mas grande mas lento
    imagen = noise(imagen)
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    if(HSV):
        if(not ON):
            #Creamos una ventana llamada 'HSV' en la que habra todos los sliders
            cv2.namedWindow('HSV')
            cv2.createTrackbar('H min','HSV',0,180,nothing)
            cv2.createTrackbar('H max','HSV',0,180,nothing)
            cv2.createTrackbar('S min','HSV',0,255,nothing)
            cv2.createTrackbar('S max','HSV',0,255,nothing)
            cv2.createTrackbar('V min','HSV',0,255,nothing)
            cv2.createTrackbar('V max','HSV',0,255,nothing)
            ON = True

        #Los valores maximo y minimo de H,S y V se guardan en funcion de la posicion de los sliders
        hMin = cv2.getTrackbarPos('H min','HSV')
        hMax = cv2.getTrackbarPos('H max','HSV')
        sMin = cv2.getTrackbarPos('S min','HSV')
        sMax = cv2.getTrackbarPos('S max','HSV')
        vMin = cv2.getTrackbarPos('V min','HSV')
        vMax = cv2.getTrackbarPos('V max','HSV')

        #Se crea una mascara de prueba con los valores seleccionados
        mask_prueba = cv2.inRange(hsv, np.array([hMin,sMin,vMin], dtype=np.uint8),
                                  np.array([hMax, sMax, vMax], dtype=np.uint8))
        
        k = cv2.waitKey(5) & 0xFF
        #Al presionar la tecla space se guardan los valores en la lista colores
        if k == 32: #tecla space
            colores.append((np.array([hMin,sMin,vMin], dtype=np.uint8),
                            np.array([hMax,sMax,vMax], dtype=np.uint8)))
            print 'Guardado'

        #Al presionar la tecla o se cierra la ventana para escoger colores
        elif k == 111: #tecla o
            cv2.destroyWindow('HSV')
            HSV = False
            print 'Cerrado'

    #Si ya no se estan escogiendo colores
    if(not HSV):
        mask = noise(cv2.inRange(hsv, colores[0][0], colores[0][1]))
        contorno(mask)
        for col in colores[1:]:
            a = noise(cv2.inRange(hsv, col[0], col[1]))
            contorno(a)
            mask += a
            
    elif(HSV):
        mask = noise(mask_prueba)
        
    color = cv2.bitwise_and(imagen, imagen, mask= mask)
    
    if(HSV):
        #Mostramos las imagenes
        cv2.imshow('Filtrado', color)
    else:
        cv2.destroyWindow('Filtrado')
        
    cv2.imshow('Camara', imagen)

    #Termina con la tecla ESC
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break

captura.release()
cv2.destroyAllWindows()
restart()
