#v0
#Se obtienen los colores por click, se pueden guardar todos los colores
#que se quieran. Se guardan los colores con space y se termina de
#seleccionar con o

import cv2, sys, os, math
import numpy as np

colores = []
px = [0,0,0]
hue = [0,0]
clk = False

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

def click(event, x, y, flags, param):
    global px, hue, clk
    
    #Cuando se hace click la funcion toma el valor del pixel
    if event == cv2.EVENT_LBUTTONDOWN and HSV:
        clk = True
        px = imagen[y, x]           #Valor del pixel en BRG
        px_hsv = cv2.cvtColor(np.uint8([[px]]),
                              cv2.COLOR_BGR2HSV)#Valor del pixel en HSV
        px_hue = px_hsv[0][0]                   #Hue del pixel
        '''print x, y                  #Coord del pixel
        print px                    #Pixel BGR
        print px_hsv                #Pixel HSV'''

        if px_hue[0] - 20 < 0:
            huemin = 0
        else:
            huemin = px_hue[0] - 20

        if px_hue[0] + 20 > 180:
            huemax = 180
        else:
            huemax = px_hue[0] + 20

        hue = [huemin, huemax]


#Iniciamos la camara
captura = cv2.VideoCapture(0)

#Se crea la ventana camara y el handler para el click
cv2.namedWindow("Camara")
cv2.setMouseCallback("Camara", click)

while(1):

    #Capturamos una imagen y la convertimos de RGB -> HSV
    _,imagen = captura.read()
    #imagen = cv2.blur(imagen,(3,3))
    #Se le aplican diferentes filtros
    imagen = cv2.bilateralFilter(imagen,5,75,75) #5 o 9, mas grande mas lento
    imagen = noise(imagen)
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    if(HSV):
        
        #Se crea una mascara de prueba con los valores seleccionados
        mask_prueba = cv2.inRange(hsv, np.array([hue[0],70,70], dtype=np.uint8),
                                  np.array([hue[1], 255, 255], dtype=np.uint8))
        
        k = cv2.waitKey(5) & 0xFF
        #Al presionar la tecla space se guardan los valores en la lista colores
        if k == 32: #tecla space
            colores.append((np.array([hue[0],70,70], dtype=np.uint8),
                            np.array([hue[1], 255, 255], dtype=np.uint8)))
            print 'Guardado'

        #Al presionar la tecla o se cierra la ventana para escoger colores
        elif k == 111: #tecla o
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
