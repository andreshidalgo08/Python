#Se utiliza para comunicacion serial
#en otro archivo se abre el COM2 y se envia con ser.write('bla')
import win32api, time, serial, sys, os, threading

def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def leer(): #Lee del micro un byte lo convierte a int y lo regresa
    while(1):
        com=ser.read(1) #Lee hasta 1 bytes
        if len(com) > 0:
            print com, ord(com)
        else:
            pass

def esc():
    while(1):
        if win32api.GetAsyncKeyState(0x1B) < 0:
            print 'fin'
            ser.close()
            restart()

ser = serial.Serial('COM2',2400,timeout=1) #Abre el puerto COM1 a baudrate 115200
print (ser.name)

task1 = threading.Thread(target=leer)
task2 = threading.Thread(target=esc)
task1.start()
task2.start()
