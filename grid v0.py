#[H-10, 100,100] and [H+10, 255, 255]
#adaptive thresholding
#gaussianBlur
#Camshift
import cv2, sys, os, math
import numpy as np

x, y = 0, 0
clk = False
px = []

#Definimos las funciones
#Reinicia el shell para apagar la comunicacion con la camara
def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def click(event, x, y, flags, param):
    global clk, px
    
    #Cuando se hace click la funcion toma el valor del pixel
    if event == cv2.EVENT_LBUTTONDOWN:
        clk = True
        px = [x, y]

                

#Iniciamos la camara
captura = cv2.VideoCapture(0)
_,imagen = captura.read()

#Se crea la ventana camara y el handler para el click
cv2.namedWindow("Camara")
cv2.setMouseCallback("Camara", click)

height, width, _ = imagen.shape
print width, height

while(1):
    #Capturamos una imagen y la convertimos de RGB -> HSV
    _,imagen = captura.read()
    imagen = cv2.bilateralFilter(imagen,5,75,75) #5 0 9, mas grande mas lento

    for i in range(1, width/20):
        imagen = cv2.line(imagen,(i*20,0),(i*20,height),(255,255,255),1)

    for i in range(1, height/20):
        imagen = cv2.line(imagen,(0,i*20),(width,i*20),(255,255,255),1)
        
    if clk:
        imagen = cv2.rectangle(imagen,((px[0]/20)*20,(px[1]/20)*20),
                               ((px[0]/20+1)*20,(px[1]/20+1)*20),(0,255,0),-1)
    
    #Mostramos las imagenes
    cv2.imshow('Camara', imagen)

    #Termina con la tecla ESC
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break

captura.release()
cv2.destroyAllWindows()
restart()
