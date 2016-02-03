from serial import *
import serial.tools.list_ports
import datetime, time

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
  if serialBuffer.find("Moisture Reading:") != -1:
    reading = serialBuffer.split("Moisture Reading:")[1].strip()

    if int(reading) < 500:
      currentDatetime = datetime.datetime.utcnow()
      print "Watered Plant at " + currentDatetime.strftime("%H:%M:%S")
      # sprayBottleInterface.spritzOnce()

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
