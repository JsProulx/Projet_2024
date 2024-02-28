import serial
import time

def is_ttyS0_available():
    try:
        ser = serial.Serial('/dev/ttyUSB0')
        ser.close()
        return True
    except serial.SerialException:
        return False
if is_ttyS0_available():
    print("dispo")
else:
    print("indispo")

#Configuration du serial port
serial_Port = serial.Serial('/dev/ttyUSB0', 9600)



while True:
    line = serial_Port.readline().decode()
    print(line)