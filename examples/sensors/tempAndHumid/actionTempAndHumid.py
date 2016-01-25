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

def parseBuffer(serialBuffer):
  if serialBuffer.find("Temperature Reading:") != -1:
    reading = serialBuffer.split("Temperature Reading:")[1].strip()

    fileDate = datetime.date.today()
    fileName = "TempAndHumidLog_" + fileDate.isoformat() + ".txt"
    logFile = open(fileName, 'a')
    logTime = datetime.datetime.utcnow()
    logFile.write(logTime.strftime("%H:%M:%S") + " " + reading + "\n")
    logFile.close()
    
  if serialBuffer.find("Humidity Reading:") != -1:
    reading = serialBuffer.split("Humidity Reading:")[1].strip()

    fileDate = datetime.date.today()
    fileName = "TempAndHumidLog_" + fileDate.isoformat() + ".txt"
    logFile = open(fileName, 'a')
    logTime = datetime.datetime.utcnow()
    logFile.write(logTime.strftime("%H:%M:%S") + " " + reading + "\n")
    logFile.close()

print "\nCtrl-C to close COM port and exit.\n"

try:
  while (1):
    readLetter = serialPort.read() 
    
    if readLetter == "\n":
      print serialBuffer
      parseBuffer(serialBuffer)
      serialBuffer = ""

    else:
      serialBuffer += readLetter

    time.sleep(0.05)
except KeyboardInterrupt:
  print "\nClosing COM port and exiting.\n"

serialPort.close()
