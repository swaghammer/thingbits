import httplib, urllib
from serial import *
import serial.tools.list_ports
import time

ports = sorted(serial.tools.list_ports.comports())
i = 1
for elem in ports:
  print i, " - " + elem[0]
  i = i + 1
selectedPort = input("Select COM port option: ")
comPort = ports[selectedPort - 1][0]

serialPort = Serial(comPort, 57600, timeout=0, writeTimeout=0)
serialBuffer = ""
  
def parseBuffer(serialBuffer):
  if serialBuffer.find("|") == -1:
    print serialBuffer
    return lastTextTime
  parsedPacket = parsePacket(serialBuffer)
  if parsedPacket != False:
    if parsedPacket['sensorType'] == 'SND':
      if parsedPacket['sensorID'] == 'Ninja':
        if parsedPacket['payload'] == "Sound":
          print time.strftime("%Y-%m-%d %H:%M:%S|") + serialBuffer.strip()
          print "\nThe ninja made too much noise!\n\n"

print "\nCtrl-C to close COM port and exit.\n"

try:
  while (1):
    readLetter = serialPort.read() 
    
    if readLetter == "\n":
      parseBuffer(serialBuffer)
      serialBuffer = ""

    else:
      serialBuffer += readLetter

    time.sleep(0.05)
except KeyboardInterrupt:
  print "\nClosing COM port and exiting.\n"

serialPort.close()
