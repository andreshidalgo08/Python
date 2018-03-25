#Se utiliza para controla la velocidad de los motores mientras se prueba
import sys, os, win32api, time, serial

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

ser = serial.Serial('COM1',115200,timeout=1) #Abre el puerto COM1 a baudrate 115200
print (ser.name)

while(1):

    if win32api.GetAsyncKeyState(VK_CODE['spacebar']) < 0:
        if direccion == 0:
            direccion = 1
        else:
            direccion =0
        print direccion
        
    elif win32api.GetAsyncKeyState(VK_CODE['up_arrow']) < 0:
        dutycicle += 1
        print dutycicle
        
    elif win32api.GetAsyncKeyState(VK_CODE['down_arrow']) < 0:
        dutycicle -= 1
        print dutycicle
        
    elif win32api.GetAsyncKeyState(VK_CODE['esc']) < 0:
        break

    time.sleep(0.1)

print 'fin'
ser.close()
restart()
