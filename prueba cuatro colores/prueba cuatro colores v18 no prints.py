#v18
#Se identifican los obstaculos

import cv2, sys, os, serial
import numpy as np

filtros = []

kernel = np.ones((3, 3), np.uint8)

HSV = True
ON = False
pista = True
cruces = True
der = False
izq = False
arr = False
aba = False
para = False
entrecruce = False

grid = 5
rad = 35
ladox = 70
ladoy = 50
meta = (-1,-1)
vladi = (-1,-1)
vladi2 = (-1,-1)
dirx = 1#1: der, 2: izq, 0: aba o arr
diry = 0#1: aba, 2: arr, 0: izq o der
giri = 107
gird = 97
rect = 77
alto = 117

px = []
pxpista = []
pxcruces = []
remove = []
primera = []
segunda = []
tercera = []
obstaculos = []

#Definimos las funciones
def nothing(x):
    pass

#Reinicia el shell para terminar por completo el programa
def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)

#Envia por serial
def enviar(comando):
    print 'enviado ', comando, chr(comando)
    ser.write(chr(comando))
    
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
        
        imagen = cv2.circle(imagen,(px[0], px[1]),rad,(255, 255, 255),2)
        
        #Dibujamos una marca en el centro del objeto
        cv2.rectangle(imagen, (px[0], px[1]), (px[0] + 2, px[1] + 2),(255,255,255), 2)
        
#Para ordenar los puntos para seleccionar la pista
def order_points(pts):
    
    rect = np.zeros((4, 2), dtype = "float32")
    
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    
    return rect

#Para ordenar los puntos para seleccionar la pista
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

#Calculo de distancia entre dos puntos
def distancia(p,q):
    return np.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

#Para ordenar los cruces
def ordenarx(linea, n):
    global pxcruces
    for indx in linea:
        if pxcruces[indx].centro[0] < width/4:
            pxcruces[indx].pos = (0,n)
        elif pxcruces[indx].centro[0] > width/4 and pxcruces[indx].centro[0] < width/2:
            pxcruces[indx].pos = (1,n)
        elif pxcruces[indx].centro[0] > width/2 and pxcruces[indx].centro[0] < 3*width/4:
            pxcruces[indx].pos = (2,n)
        elif pxcruces[indx].centro[0] > 3*width/4:
            pxcruces[indx].pos = (3,n)

#Handlers
def click(event, x, y, flags, param):
    global px, hue, pista, cruces, remove, i, j

    #Para delimitar la pista
    if event == cv2.EVENT_LBUTTONDOWN and pista:
        pxpista.append((x, y))
        
        if len(pxpista) == 4:
            pista = False

    #Para seleccionar los cruces
    elif event == cv2.EVENT_LBUTTONDOWN and cruces:
        repetido = False
        for cr in pxcruces:
            if (x > cr.centro[0] - ladox and x < cr.centro[0] + ladox and 
                y > cr.centro[1] - ladoy and y < cr.centro[1] + ladoy):
                remove.append(cr)
                repetido = True

        if not repetido:
            pxcruces.append(cruce((x, y)))
            
        else:
            pxcruces.remove(remove[0])
            remove = []
        
        if len(pxcruces) == 12:
            for cr in pxcruces:
                if cr.centro[1] < height/3:
                    primera.append(pxcruces.index(cr))
                elif cr.centro[1] > height/3 and cr.centro[1] < 2*height/3:
                    segunda.append(pxcruces.index(cr))
                elif cr.centro[1] > 2*height/3:
                    tercera.append(pxcruces.index(cr))

            ordenarx(primera, 0)
            ordenarx(segunda, 1)
            ordenarx(tercera, 2)

            print 'Cruces listos'
            cruces = False

    #Para cambiar la meta
    elif event == cv2.EVENT_LBUTTONDOWN:
        cambiar = False
        for cr in pxcruces:
            if (x > cr.centro[0] - ladox and x < cr.centro[0] + ladox and 
                y > cr.centro[1] - ladoy and y < cr.centro[1] + ladoy):
                cambiar = True

        if cambiar:
            for cr in pxcruces:
                if (x > cr.centro[0] - ladox and x < cr.centro[0] + ladox and
                    y > cr.centro[1] - ladoy and y < cr.centro[1] + ladoy):
                    cr.color = (0,0,255)
                    cr.meta = True
                    meta = cr.pos
                else:
                    cr.color = (255,255,255)
                    cr.meta = False

#Class
class filtro:

    def __init__(self, color, centro = [0, 0], danger = False, vlad = False):
        self.vladi = vlad
        self.color = color
        self.centro = [centro[0], centro[1]]
        self.danger = danger

class cruce:

    def __init__(self, centro, color = (255,255,255), meta = False, pos = (0,0)):
        self.meta = meta
        self.centro = centro
        self.color = color
        self.pos = pos

#main
#Abre el puerto COM3 a baudrate 2400
#ser = serial.Serial('COM3',2400,timeout=1)
#print (ser.name)

#Iniciamos la camara
captura = cv2.VideoCapture(0)

_,imagen = captura.read()

height, width, _ = imagen.shape

#Se crea la ventana camara y el handler para el click
cv2.namedWindow("Camara")
cv2.setMouseCallback("Camara", click)

while(1):

    #Capturamos una imagen y la convertimos de RGB -> HSV
    _,imagen = captura.read()

    #Transformacion trigonometrica
    if not pista:
        pts = np.array(pxpista, dtype = "float32")
        imagen = four_point_transform(imagen, pts)
        height, width, _ = imagen.shape
    
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
                print 'Vladi1000'
                
            print 'Guardado'

            cv2.setTrackbarPos('S min','HSV',2)
            cv2.setTrackbarPos('S max','HSV',255)
            cv2.setTrackbarPos('V min','HSV',0)
            cv2.setTrackbarPos('V max','HSV',255)

        #Al presionar la tecla o se cierra la ventana para escoger colores
        elif k == 111: #tecla o
            cv2.destroyWindow('HSV')
            HSV = False
            print 'Cerrado'

    #Si ya no se estan escogiendo colores
    if not HSV and len(filtros) > 0:
        #Se crea la mask de el primer filtro
        mask = noise(cv2.inRange(hsv, filtros[0].color[0], filtros[0].color[1]))
        contorno(mask)
        filtros[0].centro = px
        filtros[0].danger = False

        #Se crean las demas mask y se juntan en una sola
        for fil in filtros[1:]:
            a = noise(cv2.inRange(hsv, fil.color[0], fil.color[1]))
            contorno(a)
            fil.centro = px
            fil.danger = False
            mask += a

    #Se usa la mask de prueba
    elif(HSV):
        mask = noise(mask_prueba)

        #Aplico la mascara        
        color = cv2.bitwise_and(imagen, imagen, mask= mask)
    
    if HSV:
        #Mostramos el filtrado
        cv2.imshow('Filtrado', color)
    else:
        cv2.destroyWindow('Filtrado')
        
    #Se escoge el color de los cruces
    #Se le atribuyen al carro y a los obstaculos las posiciones donde se ubican
    entrecruce = True
    if not cruces and not HSV:
        obstaculos = []
        for cr in pxcruces:
            if (filtros[0].centro[0] > cr.centro[0] - ladox and filtros[0].centro[0] < cr.centro[0] + ladox and
                filtros[0].centro[1] > cr.centro[1] - ladoy and filtros[0].centro[1] < cr.centro[1] + ladoy):
                cr.color = (0,255,0)
                vladi = cr.pos
                entrecruce = False
                #if cerca de un lado u otro, se ponen dirx y diry
                
            elif not cr.meta:
                cr.color = (255,255,255)
                
            elif cr.meta:
                cr.color = (0,0,255)

            for fil in filtros[1:]:
                if (filtros[0].centro[0] > cr.centro[0] - ladox and filtros[0].centro[0] < cr.centro[0] + ladox and
                    filtros[0].centro[1] > cr.centro[1] - ladoy and filtros[0].centro[1] < cr.centro[1] + ladoy):
                    obstaculos.append(cr.pos)

    #si no se esta en un cruce se manda 255
    if entrecruce:
        enviar(255)

    #Dibujar los cruces
    if len(pxcruces) > 0:
        for cr in pxcruces:
            cv2.rectangle(imagen, (cr.centro[0] - ladox, cr.centro[1] - ladoy), (cr.centro[0] + ladox, cr.centro[1] + ladoy),cr.color, 2)

    #Despues de escoger
    if not HSV:
        
        #Chequeo de choque
        for fil in filtros[1:]:
            if distancia(filtros[0].centro, fil.centro) < 2*rad:
                fil.danger = True
                if not para:
                    para = True
                    print 'PARA!'
                    enviar(alto)
                
        #Se escoge el color de los centros  
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

        #UDRL 77, 97, 107, 117, cambiar la distancia para ver si tengo algo
        #cerca, valores entre 0-0-0 la mitad del primer - y el tercer 0
        #Imprime la posicion de los otros carros con respecto a vladi
        '''
        if meta != (-1,-1) and vladi != (-1,-1):

            if vladi != vladi2 or para:
                px1 = filtros[0].centro
                der = False
                izq = False
                arr = False
                aba = False
                for fil in filtros[1:]:
                    print fil.centro, px1
                    if (fil.centro[0] > px1[0] + 120 and fil.centro[0] < px1[0] + 180
                        and fil.centro[1] > px1[1] - rad and fil.centro[1] < px1[1] + rad):
                        print 'Obstaculo a la derecha'
                        der = True

                    if (fil.centro[0] > px1[0] - 180 and fil.centro[0] < px1[0] - 120
                          and fil.centro[1] > px1[1] - rad and fil.centro[1] < px1[1] + rad):
                        print 'Obstaculo a la izquierda'
                        izq = True

                    #150, 90
                    if (fil.centro[0] > px1[0] - rad and fil.centro[0] < px1[0] + rad
                          and fil.centro[1] > px1[1] - 110 and fil.centro[1] < px1[1] - 50):
                        print 'Obstaculo arriba'
                        arr = True

                    if (fil.centro[0] > px1[0] - rad and fil.centro[0] < px1[0] + rad
                          and fil.centro[1] > px1[1] + 50 and fil.centro[1] < px1[1] + 110):
                        print 'Obstaculo abajo'
                        aba = True
                        '''
        #Se especifica si se encuentra un obstaculo cerca
        der = False
        izq = False
        arr = False
        aba = False
        for obs in obstaculos:
            if obs[0] == vladi[0] and obs[1] == vladi[1] - 1:
                print 'Obstaculo arriba'
                arr = True

            elif obs[0] == vladi[0] and obs[1] == vladi[1] + 1:
                print 'Obstaculo abajo'
                aba = True
                
            elif obs[1] == vladi[1] and obs[0] == vladi[0] - 1:
                print 'Obstaculo a la izquierda'
                izq = True

            elif obs[1] == vladi[1] and obs[0] == vladi[0] + 1:
                print 'Obstaculo a la derecha'
                der = True
                
        #Calculo de ruta
        #Si ya se ubicoel carro y se selecciono la meta se puede proceder
        if meta != (-1,-1) and vladi != (-1,-1):

            #Si la posicion del carro es diferente a la anterior o se
            #encuentra parado se procede
            if vladi != vladi2 or para:
                print 'der:',der,'izq:',izq,'arr:',arr,'aba:',aba
                vladi2 = vladi
                #Para ir a la izquierda
                if vladi[0] > meta[0] and dirx == 2:#hacia izq dir izq
                    if not izq:
                        para = False
                        print 'recto izq'
                        enviar(rect)
                    elif vladi[1] > meta[1]:
                        if not arr and vladi[1] != 0:
                            dirx = 0
                            diry = 2
                            para = False
                            print 'gira der'#gira hacia arr
                            enviar(gird)
                        elif not aba and vladi[1] != 2:
                            dirx = 0
                            diry = 1
                            para = False
                            print 'gira izq'#gira hacia aba
                            enviar(giri)
                        else:
                            if not para:
                                para = True
                                print 'PARA!'
                                enviar(alto)
                    elif vladi[1] <= meta[1]:
                        if not aba and vladi[1] != 2:
                            dirx = 0
                            diry = 1
                            para = False
                            print 'gira izq'#gira hacia aba
                            enviar(giri)
                        elif not arr and vladi[1] != 0:
                            dirx = 0
                            diry = 2
                            para = False
                            print 'gira der'#gira hacia arr
                            enviar(gird)
                        else:
                            if not para:
                                para = True
                                print 'PARA!'
                                enviar(alto)
                                
                elif vladi[0] > meta[0] and dirx == 1:#hacia izq dir der
                    if vladi[1] > meta[1]:
                        if not arr:
                            dirx = 0
                            diry = 2
                            para = False
                            print 'gira izq'#gira hacia arr
                            enviar(giri)
                        elif not aba and vladi[1] != 2:
                            dirx = 0
                            diry = 1
                            para = False
                            print 'gira der'#gira hacia aba
                            enviar(gird)
                        elif not der and vladi[0] != 3:
                            para = False
                            print 'recto der'
                            enviar(rect)
                        else:
                            if not para:
                                para = True
                                print 'PARA!'
                                enviar(alto)
                    
                    elif vladi[1] < meta[1]:
                        if not aba:
                            dirx = 0
                            diry = 1
                            para = False
                            print 'gira der'#gira hacia aba
                            enviar(gird)
                        elif not arr and vladi[1] != 0:
                            dirx = 0
                            diry = 2
                            para = False
                            print 'gira izq'#gira hacia arr
                            enviar(giri)
                        elif not der and vladi[0] != 3:
                            para = False
                            print 'recto der'
                            enviar(rect)
                        else:
                            if not para:
                                para = True
                                print 'PARA!'
                                enviar(alto)
                            
                    elif vladi[1] == meta[1]:
                        if vladi[1] == 0:
                            if not aba:
                                dirx = 0
                                diry = 1
                                para = False
                                print 'gira der'#gira hacia aba
                                enviar(gird)
                            elif not der and vladi[0] != 3:
                                para = False
                                print 'recto der'
                                enviar(rect)
                            else:
                                if not para:
                                    para = True
                                    print 'PARA!'
                                    enviar(alto)
                                
                        elif vladi[1] == 1:
                            if not arr:
                                dirx = 0
                                diry = 2
                                para = False
                                print 'gira izq'#gira hacia arr
                                enviar(giri)
                            elif not aba:
                                dirx = 0
                                diry = 1
                                para = False
                                print 'gira der'#gira hacia aba
                                enviar(gird)
                            elif not der and vladi[0] != 3:
                                para = False
                                print 'recto der'
                                enviar(rect)
                            else:
                                if not para:
                                    para = True
                                    print 'PARA!'
                                    enviar(alto)
                                
                        elif vladi[1] == 2:
                            if not arr:
                                dirx = 0
                                diry = 2
                                para = False
                                print 'gira izq'#gira hacia arr
                                enviar(giri)
                            elif not der and vladi[0] != 3:
                                para = False
                                print 'recto der'
                                enviar(rect)
                            else:
                                if not para:
                                    para = True
                                    print 'PARA!'
                                    enviar(alto)
                                
                elif vladi[0] > meta[0] and diry == 1:#hacia izq dir aba
                    if not izq:
                        diry = 0
                        dirx = 2
                        para = False
                        print 'girar der'#gira hacia izq
                        enviar(gird)
                    elif not aba and vladi[1] != 2:
                        para = False
                        print 'recto aba'
                        enviar(rect)
                    elif not der and vladi[0] != 3:
                        diry = 0
                        dirx = 1
                        para = False
                        print 'girar izq'#gira hacia der
                        enviar(giri)
                    else:
                        if not para:
                            para = True
                            print 'PARA!'
                            enviar(alto)
                
                elif vladi[0] > meta[0] and diry == 2:#hacia izq dir arr
                    if not izq:
                        diry = 0
                        dirx = 2
                        para = False
                        print 'girar izq'#gira hacia izq
                        enviar(giri)
                    elif not arr and vladi[1] != 0:
                        para = False
                        print 'recto arr'
                        enviar(rect)
                    elif not der and vladi[0] != 3:
                        diry = 0
                        dirx = 1
                        para = False
                        print 'girar der'#gira hacia der
                        enviar(gird)
                    else:
                        if not para:
                            para = True
                            print 'PARA!'
                            enviar(alto)

                #Para ir a la derecha
                if vladi[0] < meta[0] and dirx == 1:#hacia der dir der
                    if not der:
                        para = False
                        print 'recto der'
                        enviar(rect)
                    elif vladi[1] > meta[1]:
                        if not arr and vladi[1] != 0:
                            dirx = 0
                            diry = 2
                            para = False
                            print 'gira izq'#gira hacia arr
                            enviar(giri)
                        elif not aba and vladi[1] != 2:
                            dirx = 0
                            diry = 1
                            para = False
                            print 'gira der'#gira hacia aba
                            enviar(gird)
                        else:
                            if not para:
                                para = True
                                print 'PARA!'
                                enviar(alto)
                                
                    elif vladi[1] <= meta[1]:
                        if not aba and vladi[1] != 2:
                            dirx = 0
                            diry = 1
                            para = False
                            print 'gira der'#gira hacia aba
                            enviar(gird)
                        elif not arr and vladi[1] != 0:
                            dirx = 0
                            diry = 2
                            para = False
                            print 'gira izq'#gira hacia arr
                            enviar(giri)
                        else:
                            if not para:
                                para = True
                                print 'PARA!'
                                enviar(alto)
                                
                elif vladi[0] < meta[0] and dirx == 2:#hacia der dir izq
                    if vladi[1] > meta[1]:
                        if not arr:
                            dirx = 0
                            diry = 2
                            para = False
                            print 'gira der'#gira hacia arr
                            enviar(gird)
                        elif not aba and vladi[1] != 2:
                            dirx = 0
                            diry = 1
                            para = False
                            print 'gira izq'#gira hacia aba
                            enviar(giri)
                        elif not izq and vladi[0] != 0:
                            para = False
                            print 'recto izq'
                            enviar(rect)
                        else:
                            if not para:
                                para = True
                                print 'PARA!'
                                enviar(alto)
                    
                    elif vladi[1] < meta[1]:
                        if not aba:
                            dirx = 0
                            diry = 1
                            para = False
                            print 'gira izq'#gira hacia aba
                            enviar(giri)
                        elif not arr and vladi[1] != 0:
                            dirx = 0
                            diry = 2
                            para = False
                            print 'gira der'#gira hacia arr
                            enviar(gird)
                        elif not izq and vladi[0] != 0:
                            para = False
                            print 'recto izq'
                            enviar(rect)
                        else:
                            if not para:
                                para = True
                                print 'PARA!'
                                enviar(alto)
                            
                    elif vladi[1] == meta[1]:
                        if vladi[1] == 0:
                            if not aba:
                                dirx = 0
                                diry = 1
                                para = False
                                print 'gira izq'#gira hacia aba
                                enviar(giri)
                            elif not izq and vladi[0] != 0:
                                para = False
                                print 'recto izq'
                                enviar(rect)
                            else:
                                if not para:
                                    para = True
                                    print 'PARA!'
                                    enviar(alto)
                                
                        elif vladi[1] == 1:
                            if not arr:
                                dirx = 0
                                diry = 2
                                para = False
                                print 'gira der'#gira hacia arr
                                enviar(gird)
                            elif not aba:
                                dirx = 0
                                diry = 1
                                para = False
                                print 'gira izq'#gira hacia aba
                                enviar(giri)
                            elif not izq and vladi[0] != 0:
                                para = False
                                print 'recto izq'
                                enviar(rect)
                            else:
                                if not para:
                                    para = True
                                    print 'PARA!'
                                    enviar(alto)
                                
                        elif vladi[1] == 2:
                            if not arr:
                                dirx = 0
                                diry = 2
                                para = False
                                print 'gira der'#gira hacia arr
                                enviar(gird)
                            elif not izq and vladi[0] != 0:
                                para = False
                                print 'recto izq'
                                enviar(rect)
                            else:
                                if not para:
                                    para = True
                                    print 'PARA!'
                                    enviar(alto)
                                
                elif vladi[0] < meta[0] and diry == 1:#hacia der dir aba
                    if not der:
                        diry = 0
                        dirx = 1
                        para = False
                        print 'girar izq'#gira hacia der
                        enviar(giri)
                    elif not aba and vladi[1] != 2:
                        para = False
                        print 'recto aba'
                        enviar(rect)
                    elif not izq and vladi[0] != 0:
                        diry = 0
                        dirx = 2
                        para = False
                        print 'girar der'#gira hacia izq
                        enviar(gird)
                    else:
                        if not para:
                            para = True
                            print 'PARA!'
                            enviar(alto)
                
                elif vladi[0] < meta[0] and diry == 2:#hacia der dir arr
                    if not der:
                        diry = 0
                        dirx = 1
                        para = False
                        print 'girar der'#gira hacia der
                        enviar(gird)
                    elif not arr and vladi[1] != 0:
                        para = False
                        print 'recto arr'
                        enviar(rect)
                    elif not izq and vladi[0] != 0:
                        diry = 0
                        dirx = 2
                        para = False
                        print 'girar izq'#gira hacia izq
                        enviar(giri)
                    else:
                        if not para:
                            para = True
                            print 'PARA!'
                            enviar(alto)
                    
                elif vladi[0] == meta[0]:
                    print 'x listo'
                    if dirx == 1:
                        if vladi[1] > meta[1]:#hacia arr dir der
                            if not arr:
                                dirx = 0
                                diry = 2
                                para = False
                                print 'girar izq'#gira hacia arr
                                enviar(giri)
                            elif not der and vladi[0] != 3:
                                para = False
                                print 'recto der'
                                enviar(rect)
                            elif not aba and vladi[1] != 2:
                                dirx = 0
                                diry = 1
                                para = False
                                print 'girar der'#gira hacia aba
                                enviar(gird)
                            else:
                                if not para:
                                    para = True
                                    print 'PARA!'
                                    enviar(alto)
                                    
                        elif vladi[1] < meta[1]:#hacia aba dir der
                            if not aba:
                                dirx = 0
                                diry = 1
                                para = False
                                print 'girar der'#gira hacia aba
                                enviar(gird)
                            elif not der and vladi[0] != 3:
                                para = False
                                print 'recto der'
                                enviar(rect)
                            elif not arr and vladi[1] != 0:
                                dirx = 0
                                diry = 2
                                para = False
                                print 'girar izq'#gira hacia arr
                                enviar(giri)
                            else:
                                if not para:
                                    para = True
                                    print 'PARA!'
                                    enviar(alto)

                        elif vladi[1] == meta[1]:
                            print 'LISTO'
                            vladi2 = (-1,-1)
                            meta = (-1,-1)
                    elif dirx == 2:
                        if vladi[1] > meta[1]:#hacia arr dir izq
                            if not arr:
                                dirx = 0
                                diry = 2
                                para = False
                                print 'girar der'#gira hacia arr
                                enviar(gird)
                            elif not izq and vladi[0] != 0:
                                para = False
                                print 'recto izq'
                                enviar(rect)
                            elif not aba and vladi[1] != 2:
                                dirx = 0
                                diry = 1
                                para = False
                                print 'girar izq'#gira hacia aba
                                enviar(giri)
                            else:
                                if not para:
                                    para = True
                                    print 'PARA!'
                                    enviar(alto)
                                
                        elif vladi[1] < meta[1]:#hacia aba dir izq
                            if not aba:
                                dirx = 0
                                diry = 1
                                para = False
                                print 'girar izq'#gira hacia aba
                                enviar(giri)
                            elif not izq and vladi[0] != 0:
                                para = False
                                print 'recto izq'
                                enviar(rect)
                            elif not arr and vladi[1] != 0:
                                dirx = 0
                                diry = 2
                                para = False
                                print 'girar der'#gira hacia arr
                                enviar(gird)
                            else:
                                if not para:
                                    para = True
                                    print 'PARA!'
                                    enviar(alto)
                                
                        elif vladi[1] == meta[1]:
                            print 'LISTO'
                            vladi2 = (-1,-1)
                            meta = (-1,-1)
                            
                    elif vladi[1] != meta[1] and diry == 1:
                        if not aba and vladi[1] != 2:
                            para = False
                            print 'recto aba'
                            enviar(rect)
                        elif not der and vladi[0] != 3:
                            dirx = 1
                            diry = 0
                            para = False
                            print 'girar izq'#gira hacia der
                            enviar(giri)
                        elif not izq and vladi[0] != 0:
                            dirx = 2
                            diry = 0
                            para = False
                            print 'girar der'#gira hacia izq
                            enviar(gird)
                        else:
                            if not para:
                                para = True
                                print 'PARA!'
                                enviar(alto)
                            
                    elif vladi[1] != meta[1] and diry == 2:
                        if not arr and vladi[1] != 0:
                            para = False
                            print 'recto arr'
                            enviar(rect)
                        elif not der and vladi[0] != 3:
                            dirx = 1
                            diry = 0
                            para = False
                            print 'girar der'#gira hacia der
                            enviar(gird)
                        elif not izq and vladi[0] != 0:
                            dirx = 2
                            diry = 0
                            para = False
                            print 'girar izq'#gira hacia izq
                            enviar(giri)
                        else:
                            if not para:
                                para = True
                                print 'PARA!'
                                enviar(alto)
                    else:
                        print 'LISTO'
                        vladi2 = (-1,-1)
                        meta = (-1,-1)
        
    cv2.imshow('Camara', imagen)

    #Termina con la tecla ESC
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break

captura.release()
cv2.destroyAllWindows()
ser.close()
restart()
