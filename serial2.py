import serial
import time
import string


#opening serial port
time.sleep(1)
qe128 = serial.Serial(2, 115200, timeout = 1)
#probando comunicacion
qe128.write("testing...\n\r")
print qe128.name, (" conected.")

#abro el archivo wav
fo = open("Hello.wav")
st1 = fo.read()
#le anado simbolo para indicar el final del archivo y lo guardo en nuevo file
st2 = st1+"#"
f = open("wav.txt","w")
f.write (st2)
f.close()
f = open("wav.txt")
str = f.readline(1)

#ciclo para recibir instruccion del micro
opc=""
while (opc == ""):
    print ("esperando...\n")
    time.sleep(0.00125)
    opc=qe128.readline(1)
    #print opc 
    #opcion 1: envia parte del wav
    if (opc=="1"):
        print ("opc= 1, enviando")
        i=0
        while(i!=1):
            qe128.write(str)
            str = f.readline(1)
            i=i+1
        qe128.write("\n\r")
        opc=""
    #opcion 2: reinicia el archivo wav
    elif (opc=="2"):
        print ("opc= 2, reiniciar")
        f.close()
        f = open("Hello.wav")
        str = f.readline(10)
        opc=""
        qe128.write("\n\rreseted...\n\n\r")
    #opcion 0: termina programa
    elif (opc=="0"):
        f.close()
        qe128.write("\n\rprograma terminado")
        qe128.close()
        print ("programa terminado")
    else:
        print ("recibido: "), opc
        opc=""
    

        
