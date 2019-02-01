import serial

port = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=3.0)

while True:
    rcv = port.read(30)
    print(rcv)
