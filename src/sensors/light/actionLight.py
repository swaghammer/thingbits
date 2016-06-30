from serial import *
import serial.tools.list_ports
import time
import datetime

ports = sorted(serial.tools.list_ports.comports())
i = 1
for elem in ports:
  print i, " - " + elem[0]
  i = i + 1
selectedPort = input("Select COM port option: ")
comPort = ports[selectedPort - 1][0]

serialPort = Serial(comPort, 57600, timeout=0, writeTimeout=0)
serialBuffer = ""

def parsePacket(packet):
  splitPacket = packet.split("|")
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

def parseBuffer(serialBuffer, consecutiveOpen):
  if serialBuffer.find("|") == -1:
    print serialBuffer
    return
  parsedPacket = parsePacket(serialBuffer)
  if parsedPacket != False:
    if parsedPacket['sensorType'] == 'LIT':
      if parsedPacket['sensorID'] == 'Solar':
        print time.strftime("%Y-%m-%d %H:%M:%S|") + serialBuffer.strip()
        fileDate = datetime.date.today()
        fileName = "BrightnessLog_" + fileDate.isoformat() + ".txt"
        logFile = open(fileName, 'a')
        logTime = datetime.datetime.utcnow()
        logFile.write(logTime.strftime("%H:%M:%S") + " " + parsedPacket['payload'] + "\n")
        logFile.close()
        
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
