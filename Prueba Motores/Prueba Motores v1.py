#Se utiliza para controla la velocidad de los motores mientras se prueba
import sys, os, win32api, threading, serial, time

#Variables
VK_CODE = {'spacebar':0x20,
           'up_arrow':0x26,
           'down_arrow':0x28,
           'esc':0x1B
           }

dutycicle = 0
direccion = 0

#Funciones
#Reinicia el shell
def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def leer(): #Lee del micro un byte lo convierte a int y lo regresa
    com=ser.read(1) #Lee hasta 1 bytes
    bt=int.from_bytes(com,byteorder='big')
    print bt

def spacebar():
    global direccion
    while(1):
        if win32api.GetAsyncKeyState(VK_CODE['spacebar']) < 0:
            if direccion == 0:
                direccion = 1
                print 'palante'
            else:
                direccion =0
                print 'patras'
            time.sleep(0.5)

def up_arrow():
    global dutycicle
    while(1):
        if win32api.GetAsyncKeyState(VK_CODE['up_arrow']) < 0:
            dutycicle += 1
            print dutycicle
            time.sleep(0.2)

def down_arrow():
    global dutycicle
    while(1):
        if win32api.GetAsyncKeyState(VK_CODE['down_arrow']) < 0:
            dutycicle -= 1
            print dutycicle
            time.sleep(0.2)

def esc():
    while(1):
        if win32api.GetAsyncKeyState(VK_CODE['esc']) < 0:
            print 'fin'
            #ser.close()
            restart()
        
#ser = serial.Serial(0,115200,timeout=1) #Abre el puerto COM1 a baudrate 115200
#print (ser.name)

task1 = threading.Thread(target=spacebar)
task1.start()

task2 = threading.Thread(target=up_arrow)
task2.start()

task3 = threading.Thread(target=down_arrow)
task3.start()

task4 = threading.Thread(target=esc)
task4.start()
