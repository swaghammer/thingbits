import httplib, urllib
from serial import *
import serial.tools.list_ports
from time import time, sleep

ports = sorted(serial.tools.list_ports.comports())
i = 1
print "\n"
for elem in ports:
  print i, " - " + elem[0]
  i = i + 1
selectedPort = input("Select COM port option: ")
comPort = ports[selectedPort - 1][0]

serialPort = Serial(comPort, 57600, timeout=0, writeTimeout=0)
serialBuffer = ""

def parsePacket(packet):
  splitPacket = packet.split("|");
  if splitPacket[1].strip() == "Unrecognized packet":
    print packet
    return False
  parsedPacket = {'signal': splitPacket[0].strip()}
  parsedPacket['sensorType'] = splitPacket[1].strip()
  parsedPacket['sensorID'] = splitPacket[2].strip()
  parsedPacket['messageType'] = splitPacket[3].strip()
  parsedPacket['voltage'] = splitPacket[4].strip()
  parsedPacket['payload'] = splitPacket[5].strip()
  return parsedPacket

def parseBuffer(serialBuffer):
  if serialBuffer.find("|") == -1:
    print serialBuffer
    return lastTextTime
  parsedPacket = parsePacket(serialBuffer)
  if parsedPacket != False:
    if parsedPacket['sensorType'] == 'BTN':
      if parsedPacket['sensorID'] == '1':
        if parsedPacket['payload'] == "Pushed":
          print time.strftime("%Y-%m-%d %H:%M:%S|") + serialBuffer.strip()
          fileName = "customerCount.txt"
          try:
            countFile = open(fileName, 'r')
            customerCount = int(countFile.read().strip())
            countFile.close()
          except:
            customerCount = 0
          customerCount = customerCount + 1
          countFile = open(fileName, 'w')
          countFile.write(customerCount)
          countFile.close()

print "\nCtrl-C to close COM port and exit.\n"

try:
  while (1):
    readLetter = serialPort.read() 
    
    if readLetter == "\n":
      lastTextTime = parseBuffer(serialBuffer)
      serialBuffer = ""

    else:
      serialBuffer += readLetter

    sleep(0.05)
except KeyboardInterrupt:
  print "\nClosing COM port and exiting.\n"

serialPort.close()
