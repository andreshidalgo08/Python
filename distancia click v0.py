#[H-10, 100,100] and [H+10, 255, 255]
#adaptive thresholding
#gaussianBlur
#Camshift
import cv2, sys, os, math
import numpy as np

circulos = []
radio = 45
remove = []
rem = False

#Definimos las funciones
#Reinicia el shell para apagar la comunicacion con la camara
def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def click(event, x, y, flags, param):
    global rem, remove
    
    #Cuando se hace click la funcion toma el valor del pixel
    if event == cv2.EVENT_LBUTTONDOWN:

        if len(circulos)>0:
            for centro in circulos:
                if distancia(centro,(x,y))<radio:
                    rem = True
                    remove.append(centro)

        if rem:
            for centro in remove:
                circulos.remove(centro)
            remove = []
            rem = False
        else:
            circulos.append((x,y))
                

def distancia(p,q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

#Iniciamos la camara
captura = cv2.VideoCapture(0)
_,imagen = captura.read()

#Se crea la ventana camara y el handler para el click
cv2.namedWindow("Camara")
cv2.setMouseCallback("Camara", click)

while(1):
    #Capturamos una imagen y la convertimos de RGB -> HSV
    _,imagen = captura.read()
    imagen = cv2.bilateralFilter(imagen,5,75,75) #5 0 9, mas grande mas lento

    for centro in circulos:
        imagen = cv2.circle(imagen,centro,radio,(255,255,255),2)

    #Mostramos las imagenes
    cv2.imshow('Camara', imagen)

    #Termina con la tecla ESC
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break

#captura.release()
cv2.destroyAllWindows()
restart()
