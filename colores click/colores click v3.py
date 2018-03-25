#[H-10, 100,100] and [H+10, 255, 255]
#adaptive thresholding
#gaussianBlur
#Camshift
import cv2, sys, os
import numpy as np

px = [0,0,0]
hue = [0,0]
clk = False

#Definimos las funciones
#Reinicia el shell para apagar la comunicacion con la camara
def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def click(event, x, y, flags, param):
    global hue, px, clk
    
    #Cuando se hace click la funcion toma el valor del pixel
    if event == cv2.EVENT_LBUTTONDOWN:
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
    
#Dibuja el contorno y el centro del objeto con mayor area
def contorno(mask):
    global imagen
    _, contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        #Escogemos el contorno con mayor area
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

def distancia(p,q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

#Iniciamos la camara
captura = cv2.VideoCapture(0)
#imagen = cv2.imread('C:\Users\Administrador\Desktop\Imagen1.jpg')

#Se crea la ventana camara y el handler para el click
cv2.namedWindow("Camara")
cv2.setMouseCallback("Camara", click)

while(1):
    #Capturamos una imagen y la convertimos de RGB -> HSV
    _,imagen = captura.read()
    imagen = cv2.bilateralFilter(imagen,5,75,75) #5 0 9, mas grande mas lento
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, np.array([hue[0],70,70], dtype=np.uint8),
                   np.array([hue[1], 255, 255], dtype=np.uint8))

    if clk:
        contorno(mask)
    
    color = cv2.bitwise_and(imagen, imagen, mask= mask)

    #Mostramos las imagenes
    cv2.imshow('Filtrado', color)
    cv2.imshow('Camara', imagen)

    #Termina con la tecla ESC
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break

#captura.release()
cv2.destroyAllWindows()
restart()
