#v12
#Se incluye diferenciacion vladi1000 otros carros
#y ubicacion con respecto a vladi1000

import cv2, sys, os, math
import numpy as np

filtros = []

kernel = np.ones((3, 3), np.uint8)

HSV = True
ON = False
grid = 5
rad = 45
px = []

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
    global imagen, px
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
        px = [int(x), int(y)]
        centro = (int(x),int(y))
        radio = int(radius)
        #print radio
        radio = rad
        imagen = cv2.circle(imagen,centro,radio,(255, 255, 255),2)
        
        #Dibujamos una marca en el centro del objeto
        cv2.rectangle(imagen, centro, (centro[0] + 2, centro[1] + 2),(255,255,255), 2)
        
def distancia(p,q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

#Class
class filtro:

    def __init__(self, color, centro = [0, 0], danger = False, vlad = False):
        self.vladi = vlad
        self.color = color
        self.centro = [centro[0], centro[1]]
        self.danger = danger #si uno esta muy cerca de otro se vuelve rojo

#Iniciamos la camara
captura = cv2.VideoCapture(0)

_,imagen = captura.read()

height, width, _ = imagen.shape
#print width, height

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
            cv2.setTrackbarPos('S min','HSV',2)
            cv2.createTrackbar('S max','HSV',0,255,nothing)
            cv2.setTrackbarPos('S max','HSV',255)
            cv2.createTrackbar('V min','HSV',0,255,nothing)
            cv2.createTrackbar('V max','HSV',0,255,nothing)
            cv2.setTrackbarPos('V max','HSV',255)
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
            filtros.append(filtro((np.array([hMin,sMin,vMin], dtype=np.uint8),
                            np.array([hMax,sMax,vMax], dtype=np.uint8))))
            
            if len(filtros) == 1:
                filtros[0].vladi = True
                print filtros[0].vladi
                
            print 'Guardado'

        #Al presionar la tecla o se cierra la ventana para escoger colores
        elif k == 111: #tecla o
            cv2.destroyWindow('HSV')
            HSV = False
            print 'Cerrado'

    #Si ya no se estan escogiendo colores
    if not HSV and len(filtros) > 0:
        mask = noise(cv2.inRange(hsv, filtros[0].color[0], filtros[0].color[1]))
        contorno(mask)
        filtros[0].centro = px
        filtros[0].danger = False
        #print filtros[0].centro
        
        for fil in filtros[1:]:
            a = noise(cv2.inRange(hsv, fil.color[0], fil.color[1]))
            contorno(a)
            fil.centro = px
            fil.danger = False
            #print fil.centro
            mask += a
            
    elif(HSV):
        mask = noise(mask_prueba)
        
    color = cv2.bitwise_and(imagen, imagen, mask= mask)
    
    if HSV:
        #Mostramos las imagenes
        cv2.imshow('Filtrado', color)
    else:
        cv2.destroyWindow('Filtrado')

    #Grid
    if not HSV:
        for i in range(1, width/grid):
            imagen = cv2.line(imagen,(i*grid,0),(i*grid,height),(255,255,255),1)

        for i in range(1, height/grid):
            imagen = cv2.line(imagen,(0,i*grid),(width,i*grid),(255,255,255),1)

        #chequeo de choque
        for fil in filtros[:len(filtros)-1]:# otro for con [i:]
            for fil2 in filtros[filtros.index(fil)+ 1:]:
                if distancia(fil.centro, fil2.centro) < 2*rad:
                    fil.danger = True
                    fil2.danger = True
                
        #Coloreo del centro 
        for fil in filtros:
            if fil.danger:
                imagen = cv2.rectangle(imagen,((fil.centro[0]/grid)*grid,(fil.centro[1]/grid)*grid),
                                       ((fil.centro[0]/grid+1)*grid,(fil.centro[1]/grid+1)*grid),
                                       (0,0,255),-1)
            else:
                imagen = cv2.rectangle(imagen,((fil.centro[0]/grid)*grid,(fil.centro[1]/grid)*grid),
                                       ((fil.centro[0]/grid+1)*grid,(fil.centro[1]/grid+1)*grid),
                                       (0,255,0),-1)

            if fil.vladi:
                imagen = cv2.rectangle(imagen,((fil.centro[0]/grid)*grid,(fil.centro[1]/grid)*grid),
                                       ((fil.centro[0]/grid+1)*grid,(fil.centro[1]/grid+1)*grid),
                                       (255,0,0),-1)

        #UDRL
        px = filtros[0].centro
        for fil in filtros[1:]:
            if (fil.centro[0] > px[0] + rad and fil.centro[0] < px[0] + 3 * rad
                and fil.centro[1] > px[1] - rad and fil.centro[1] < px[1] + rad):
                print str(filtros.index(fil)) + 'Derecha'

            elif (fil.centro[0] > px[0] - 3 * rad and fil.centro[0] < px[0] - rad
                  and fil.centro[1] > px[1] - rad and fil.centro[1] < px[1] + rad):
                print str(filtros.index(fil)) + 'Izquierda'

            elif (fil.centro[0] > px[0] - rad and fil.centro[0] < px[0] + rad
                  and fil.centro[1] > px[1] - 3 * rad and fil.centro[1] < px[1] - rad):
                print str(filtros.index(fil)) + 'Arriba'

            elif (fil.centro[0] > px[0] - rad and fil.centro[0] < px[0] + rad
                  and fil.centro[1] > px[1] + rad and fil.centro[1] < px[1] + 3 * rad):
                print str(filtros.index(fil)) + 'Abajo'
        
    cv2.imshow('Camara', imagen)

    #Termina con la tecla ESC
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break

captura.release()
cv2.destroyAllWindows()
restart()
