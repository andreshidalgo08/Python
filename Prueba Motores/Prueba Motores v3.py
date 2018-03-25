#Se utiliza para controla la velocidad de los motores mientras se prueba
#Comunicacion serial, threading
#Se mandan las dos variables como una sola
import sys, os, win32api, threading, serial, time

#Variables
VK_CODE = {'spacebar':0x20,
           'up_arrow':0x26,
           'down_arrow':0x28,
           'esc':0x1B,
           'right_arrow':0x27,
           'left_arrow':0x25
           }

dutycycle = 0
direccion = 0

#Funciones
#Reinicia el shell
def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def enviar():
    dato = dutycycle + direccion
    print 'enviado ', dato, chr(dato)
    ser.write(chr(dato))

def leer(): #Lee del micro un byte lo convierte a int y lo regresa
    while(1):
        com=ser.read(2)
        print com
        if len(com) > 0:
            print 'recibido', com
        else:
            print 'pass'
            pass

def spacebar():
    global direccion
    while(1):
        if win32api.GetAsyncKeyState(VK_CODE['spacebar']) < 0:
            if direccion == 0:
                direccion = 1
                #print 'palante'
            else:
                direccion =0
                #print 'patras'
            time.sleep(0.5)
            enviar()

def up_arrow():
    global dutycycle
    while(1):
        if win32api.GetAsyncKeyState(VK_CODE['up_arrow']) < 0:
            if dutycycle == 255:
                pass
            else:
                dutycycle += 10
            time.sleep(0.2)
            enviar()

def down_arrow():
    global dutycycle
    while(1):
        if win32api.GetAsyncKeyState(VK_CODE['down_arrow']) < 0:
            if dutycycle == 0:
                pass
            else:
                dutycycle -= 10
            time.sleep(0.2)
            enviar()

def esc():
    while(1):
        if win32api.GetAsyncKeyState(VK_CODE['esc']) < 0:
            print 'fin'
            ser.close()
            restart()

#Abre el puerto COM2 a baudrate 2400
ser = serial.Serial('COM4',2400,timeout=1)
print (ser.name)

print ser.write(chr(dutycycle))
print ser.write(chr(direccion))

task1 = threading.Thread(target=spacebar)
task2 = threading.Thread(target=up_arrow)
task3 = threading.Thread(target=down_arrow)
task4 = threading.Thread(target=esc)
task5 = threading.Thread(target=leer)

task1.start()
task2.start()
task3.start()
task4.start()
task5.start()
