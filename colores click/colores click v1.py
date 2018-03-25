#[H-10, 100,100] and [H+10, 255, 255]
#adaptive thresholding
#gaussianBlur
#Camshift
import cv2, sys, os
import numpy as np

px = [0,0,0]

#Definimos las funciones
#Reinicia el shell para apagar la comunicacion con la camara
def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def click(event, x, y, flags, param):
    global mask, px#, blur, Gblur, Mblur, Bblur
    #Cuando se hace click la funcion toma el valor del pixel
    if event == cv2.EVENT_LBUTTONDOWN:
        px = imagen[y, x]           #Valor del pixel en BRG
        px_hsv = cv2.cvtColor(np.uint8([[px]]),
                              cv2.COLOR_BGR2HSV)#Valor del pixel en HSV
        px_hsv = px_hsv[0][0]
        '''print x, y                  #Coord del pixel
        print px                    #Pixel BGR
        print px_hsv                #Pixel HSV'''

        if px_hsv[0] - 20 < 0:
            huemin = 0
        else:
            huemin = px_hsv[0] - 20

        if px_hsv[0] + 20 > 180:
            huemax = 180
        else:
            huemax = px_hsv[0] + 20

        mask = cv2.inRange(Bhsv, np.array([huemin,70,70], dtype=np.uint8),
                                  np.array([huemax, 255, 255], dtype=np.uint8))
    
#Dibuja el contorn y el centro del objeto con mayor area
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

        '''#Dibujamos el contorno
        cv2.drawContours(imagen, [best_cnt], 0, (255,255,255), 2)
        #Encontramos el centro
        M = cv2.moments(best_cnt)
        x,y = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        #Dibujamos una marca en el centro del objeto
        cv2.rectangle(imagen, (x, y), (x+2, y+2),(255,255,255), 2)'''

        #Minimo circulo
        (x,y),radius = cv2.minEnclosingCircle(best_cnt)
        centro = (int(x),int(y))
        radio = int(radius)
        imagen = cv2.circle(imagen,centro,radio,(int(px[0]), int(px[1]), int(px[2])),2)

def converthsv(imagen):
    return cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
    
#Iniciamos la camara
#captura = cv2.VideoCapture(0)
imagen = cv2.imread('C:\Users\Administrador\Desktop\Imagen1.jpg')

'''cv2.namedWindow("Camara")
cv2.setMouseCallback("Camara", click)
cv2.namedWindow("blur")
cv2.setMouseCallback("blur", click)
cv2.namedWindow("Gblur")
cv2.setMouseCallback("Gblur", click)
cv2.namedWindow("Mblur")
cv2.setMouseCallback("Mblur", click)'''
cv2.namedWindow("Bblur")
cv2.setMouseCallback("Bblur", click)

mask = cv2.inRange(imagen, np.array([0,0,0], dtype=np.uint8),
                   np.array([0,0,0], dtype=np.uint8))

while(1):

    #Capturamos una imagen y la convertimos de RGB -> HSV
    #_,imagen = captura.read()
    '''blur = cv2.blur(imagen,(3,3))
    hsv = converthsv(blur)
    Gblur = cv2.GaussianBlur(imagen,(3,3),0)
    Ghsv = converthsv(Gblur)
    Mblur =cv2.medianBlur(imagen,3)
    Mhsv = converthsv(Mblur)'''
    Bblur = cv2.bilateralFilter(imagen,5,75,75) #5 0 9, mas grande mas lento
    Bhsv = converthsv(Bblur)

    contorno(mask)
    
    color = cv2.bitwise_and(imagen, imagen, mask= mask)

    #Mostramos las imagenes
    cv2.imshow('Filtrado', color)
    #cv2.imshow('blur', blur)
    #cv2.imshow('Gblur', Gblur)
    #cv2.imshow('Mblur', Mblur)
    cv2.imshow('Bblur', Bblur)
    #cv2.imshow('Camara', imagen)

    #Termina con la tecla ESC
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break

#captura.release()
cv2.destroyAllWindows()
restart()
