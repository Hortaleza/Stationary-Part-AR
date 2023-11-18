import serial

# MUST USE UART3 on the embedded system

ser = serial.Serial(
    port="COM3",  ## port name
    baudrate=115200,  ## baud rate
    bytesize=8,  ## number of databits
    parity=serial.PARITY_NONE,  ## enable parity checking
    stopbits=1,  ## number of stopbits
    timeout=1,  ## set a timeout value, None for waiting forever
)

ser.write('14'.encode())
#receivedData = ser.readline() 
#print(receivedData)
ser.close()  ## remember to close the port at last
#0021:09:0011B0