import serial, io, time, string

ser = serial.Serial(2,115200,timeout=1)
print(ser.name)
time.sleep(0.5)

a=0
while a<50:
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
    a=a+1
