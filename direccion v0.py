#v0
#77 recto, 97 derecha, 107 izquierda, 117 parar
import sys, os, win32api, threading, serial, time

#Variables
VK_CODE = {'spacebar':0x20,
           'up_arrow':0x26,
           'down_arrow':0x28,
           'esc':0x1B,
           'right_arrow':0x27,
           'left_arrow':0x25
           }

direccion = 255

#Funciones
#Reinicia el shell
def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def enviar():
    dato = direccion
    print 'enviado ', dato, chr(dato)
    ser.write(chr(dato))

def spacebar():
    global direccion
    while(1):
        if win32api.GetAsyncKeyState(VK_CODE['spacebar']) < 0:
            direccion = 255
            time.sleep(0.2)
            enviar()

def up_arrow():
    global direccion
    while(1):
        if win32api.GetAsyncKeyState(VK_CODE['up_arrow']) < 0:
            direccion = 77
            time.sleep(0.2)
            enviar()

def down_arrow():
    global direccion
    while(1):
        if win32api.GetAsyncKeyState(VK_CODE['down_arrow']) < 0:
            direccion = 117
            time.sleep(0.2)
            enviar()

def left_arrow():
    global direccion
    while(1):
        if win32api.GetAsyncKeyState(VK_CODE['left_arrow']) < 0:
            direccion = 107
            time.sleep(0.2)
            enviar()

def right_arrow():
    global direccion
    while(1):
        if win32api.GetAsyncKeyState(VK_CODE['right_arrow']) < 0:
            direccion = 97
            time.sleep(0.2)
            enviar()

def esc():
    while(1):
        if win32api.GetAsyncKeyState(VK_CODE['esc']) < 0:
            print 'fin'
            ser.close()
            restart()

#Abre el puerto COM3 a baudrate 2400
ser = serial.Serial('COM3',2400,timeout=1)
print (ser.name)

print ser.write(chr(direccion))

task1 = threading.Thread(target=spacebar)
task2 = threading.Thread(target=up_arrow)
task3 = threading.Thread(target=down_arrow)
task4 = threading.Thread(target=left_arrow)
task5 = threading.Thread(target=right_arrow)
task6 = threading.Thread(target=esc)


task1.start()
task2.start()
task3.start()
task4.start()
task5.start()
task6.start()
