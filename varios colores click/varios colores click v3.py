#v3
#Pista por trigonometria, transformacion por getTransform

import cv2, sys, os
import numpy as np

filtros = []

kernel = np.ones((3, 3), np.uint8)

HSV = True
ON = False
pista = True
grid = 5
rad = 35
px1 = []
pxpista = []

px = [0,0,0]
hue = [0,0]


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
    global imagen, px1
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
        (x,y),_ = cv2.minEnclosingCircle(best_cnt)
        px1 = [int(x), int(y)]
        
        imagen = cv2.circle(imagen,(px1[0], px1[1]),rad,(255, 255, 255),2)
        
        #Dibujamos una marca en el centro del objeto
        cv2.rectangle(imagen, (px1[0], px1[1]), (px1[0] + 2, px1[1] + 2),(255,255,255), 2)
        
def order_points(pts):
    
    rect = np.zeros((4, 2), dtype = "float32")
    
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    
    return rect

def four_point_transform(image, rect):
    
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    
    widthA = distancia(br, bl)
    widthB = distancia(tr, tl)
    maxWidth = max(int(widthA), int(widthB))
    
    heightA = distancia(tr, br)
    heightB = distancia(tl, bl)
    maxHeight = max(int(heightA), int(heightB))
    
    dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype = "float32")
    
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    
    return warped

def distancia(p,q):
    return np.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

#Handlers
def click(event, x, y, flags, param):
    global px, hue, pista

    #Para delimitar la pista
    if event == cv2.EVENT_LBUTTONDOWN and pista:
        pxpista.append((x, y))
        print x, y
        
        if len(pxpista) == 4:
            pista = False
        

    #Cuando se hace click la funcion toma el valor del pixel
    elif event == cv2.EVENT_LBUTTONDOWN and HSV:
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

#Class
class filtro:

    def __init__(self, color, centro = [0, 0], danger = False, vlad = False):
        self.vladi = vlad
        self.color = color
        self.centro = [centro[0], centro[1]]
        self.danger = danger #si uno esta muy cerca de otro se vuelve rojo

#main

#Iniciamos la camara
captura = cv2.VideoCapture(0)

_,imagen = captura.read()

height, width, _ = imagen.shape
#480,640

#Se crea la ventana camara y el handler para el click
cv2.namedWindow("Camara")
cv2.setMouseCallback("Camara", click)

while(1):

    #Capturamos una imagen y la convertimos de RGB -> HSV
    _,imagen = captura.read()

    if not pista:
        pts = np.array(pxpista, dtype = "float32")
        imagen = four_point_transform(imagen, pts)
        height, width, _ = imagen.shape
    
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
            filtros.append(filtro((np.array([hue[0],70,70], dtype=np.uint8),
                                   np.array([hue[1], 255, 255], dtype=np.uint8))))
            
            if len(filtros) == 1:
                filtros[0].vladi = True
                print 'Vladi1000'
                
            print 'Guardado'

        #Al presionar la tecla o se cierra la ventana para escoger colores
        elif k == 111: #tecla o
            HSV = False
            print 'Cerrado'

    #Si ya no se estan escogiendo colores, 
    if not HSV and len(filtros) > 0:
        #Se crea la mask de el primer filtro
        mask = noise(cv2.inRange(hsv, filtros[0].color[0], filtros[0].color[1]))
        contorno(mask)
        filtros[0].centro = px1
        filtros[0].danger = False

        #Se crean las demas mask y se juntan en una sola        
        for fil in filtros[1:]:
            a = noise(cv2.inRange(hsv, fil.color[0], fil.color[1]))
            contorno(a)
            fil.centro = px1
            fil.danger = False
            mask += a

    #Se usa la mask de prueba            
    elif(HSV):
        mask = noise(mask_prueba)
        
    #Aplico la mascara    
    color = cv2.bitwise_and(imagen, imagen, mask= mask)
    
    if(HSV):
        #Mostramos el filtrado
        cv2.imshow('Filtrado', color)
    else:
        cv2.destroyWindow('Filtrado')

    #Grid
    if not HSV:
        '''
        #Se dibuja el grid
        for i in range(1, width/grid):
            imagen = cv2.line(imagen,(i*grid,0),(i*grid,height),(255,255,255),1)

        for i in range(1, height/grid):
            imagen = cv2.line(imagen,(0,i*grid),(width,i*grid),(255,255,255),1)
        '''

        #Chequeo de choque
        for fil in filtros[:len(filtros)-1]:# otro for con [i:]
            for fil2 in filtros[filtros.index(fil)+ 1:]:
                if distancia(fil.centro, fil2.centro) < 2*rad:
                    fil.danger = True
                    fil2.danger = True
                
        #Coloreo del centro 
        for fil in filtros:
            if fil.vladi:#azul
                imagen = cv2.rectangle(imagen,((fil.centro[0]/grid)*grid,(fil.centro[1]/grid)*grid),
                                       ((fil.centro[0]/grid+1)*grid,(fil.centro[1]/grid+1)*grid),
                                       (255,0,0),-1)
            elif fil.danger and not fil.vladi:#rojo
                imagen = cv2.rectangle(imagen,((fil.centro[0]/grid)*grid,(fil.centro[1]/grid)*grid),
                                       ((fil.centro[0]/grid+1)*grid,(fil.centro[1]/grid+1)*grid),
                                       (0,0,255),-1)
            else:#verde
                imagen = cv2.rectangle(imagen,((fil.centro[0]/grid)*grid,(fil.centro[1]/grid)*grid),
                                       ((fil.centro[0]/grid+1)*grid,(fil.centro[1]/grid+1)*grid),
                                       (0,255,0),-1)

        #UDRL
        #Imprime la posicion de los otros carros con respecto a vladi
        px1 = filtros[0].centro
        for fil in filtros[1:]:
            if (fil.centro[0] > px1[0] + rad and fil.centro[0] < px1[0] + 3 * rad
                and fil.centro[1] > px1[1] - rad and fil.centro[1] < px1[1] + rad):
                print str(filtros.index(fil)) + 'Derecha'

            elif (fil.centro[0] > px1[0] - 3 * rad and fil.centro[0] < px1[0] - rad
                  and fil.centro[1] > px1[1] - rad and fil.centro[1] < px1[1] + rad):
                print str(filtros.index(fil)) + 'Izquierda'

            elif (fil.centro[0] > px1[0] - rad and fil.centro[0] < px1[0] + rad
                  and fil.centro[1] > px1[1] - 3 * rad and fil.centro[1] < px1[1] - rad):
                print str(filtros.index(fil)) + 'Arriba'

            elif (fil.centro[0] > px1[0] - rad and fil.centro[0] < px1[0] + rad
                  and fil.centro[1] > px1[1] + rad and fil.centro[1] < px1[1] + 3 * rad):
                print str(filtros.index(fil)) + 'Abajo'
        
    cv2.imshow('Camara', imagen)

    #Termina con la tecla ESC
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break

captura.release()
cv2.destroyAllWindows()
restart()
