import serial, io, time, string, win32api, win32con

#Giant dictonary to hold key name and VK value
VK_CODE = {'tab':0x09,#
           'enter':0x0D,#
           'shift':0x10,#
           'ctrl':0x11,#
           'alt':0x12,#
           'esc':0x1B,#
           'spacebar':0x20,#
           'page_up':0x21,#
           'page_down':0x22,#
           'left_arrow':0x25,#
           'up_arrow':0x26,#
           'right_arrow':0x27,#
           'down_arrow':0x28,#
           'a':0x41,#
           'f':0x46,#
           'g':0x47,#
           ',':0xBC,#
           '.':0xBE,#
           }

#Faltar definir una funcion que sepa cuando se presiona la tecla 1 y para python
def escape():
    a=win32api.GetAsyncKeyState(0x08)#backspace
    if a>0:
        return 1
    else:
        return 0

def pressHoldRelease(args):
    '''
    press and hold passed in strings. Once held, release
    accepts as many arguments as you want.
    e.g. pressAndHold('left_arrow', 'a','b').
 
    this is useful for issuing shortcut command or shift commands.
    e.g. pressHoldRelease('ctrl', 'alt', 'del'), pressHoldRelease('shift','a')
    '''
    for i in args:
        win32api.keybd_event(VK_CODE[i], 0,0,0)
        time.sleep(.005)
            
    for i in args:
            win32api.keybd_event(VK_CODE[i],0 ,win32con.KEYEVENTF_KEYUP ,0)
            time.sleep(.01)

def leer(): #Lee del micro un byte lo convierte a int y lo regresa
    com=ser.read(1) #Lee hasta 1 bytes
    co1=int.from_bytes(com,byteorder='big')
    com=ser.read(1)
    co2=int.from_bytes(com,byteorder='big')
    com=ser.read(1)
    co3=int.from_bytes(com,byteorder='big')
    com=ser.read(1)
    co4=int.from_bytes(com,byteorder='big')
    co=[co1,co2,co3,co4]
    return co

#Comandos de teclado

arg1=['ctrl','alt','a']         #Inicio de Simulador
arg2=['page_up']                #Comando de teclado 1
arg3=['page_down']              #Comando de teclado 2
arg4=['left_arrow']             #Comando de teclado 3
arg5=['right_arrow']            #Comando de teclado 4
arg6=['down_arrow']             #Comando de teclado 5
arg7=['up_arrow']               #Comando de teclado 6
arg8=['shift','left_arrow']     #Comando de teclado 7
arg9=['shift','right_arrow']    #Comando de teclado 8
arg10=['f']                     #Comando de teclado 9
arg11=['shift','f']             #Comando de teclado 10
arg12=['shift','up_arrow']      #Comando de teclado 11
arg13=['shift','down_arrow']    #Comando de teclado 12
arg14=[',']                     #Comando de teclado 13
arg15=['.']                     #Comando de teclado 14
arg16=['g']                     #Comando de teclado 15
arg17=['spacebar']              #Comando de teclado 16
arg18=['ctrl']                  #Comando de teclado 17
arg19=['esc']                   #Comando de teclado 18
arg20=['tab']                   #Comando de teclado tab
arg21=['enter']                 #Comando de teclado enter

#Inicio el programa

a=0

ser = serial.Serial(1,115200,timeout=1)
print(ser.name)
time.sleep(0.5)
while a<1:
    a=escape()#Funcion para terminar el programa
    com=ser.read(1) #Lee hasta 1 bytes
    co1=int.from_bytes(com,byteorder='big')
    com=ser.read(1)
    co2=int.from_bytes(com,byteorder='big')
    com=ser.read(1)
    co3=int.from_bytes(com,byteorder='big')
    com=ser.read(1)
    co4=int.from_bytes(com,byteorder='big')
    co=[co1,co2,co3,co4]
    print(co)
    print(co[0])
    time.sleep(3)
    if co[0] == 1:
        print('Hello World')
        pressHoldRelease(arg1)#Inicia simulador
        pressHoldRelease(arg6)#Pone las preferencias de avion y aeropuerto
        pressHoldRelease(arg20)
        pressHoldRelease(arg6)
        pressHoldRelease(arg20)
        pressHoldRelease(arg6)
        pressHoldRelease(arg6)
        pressHoldRelease(arg6)
        pressHoldRelease(arg6)
        pressHoldRelease(arg6)
        pressHoldRelease(arg21)
        a=2
    else:
        print ('No valido')
