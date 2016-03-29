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
motionDetected = False
lastMotion = time.time()
availableDelay = 5 * 60

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

def setStatus(isAvailable):
  fileName = "confRoom.html"
  statusPage = open(fileName, 'w')
  color = 'red'
  if isAvailable == True:
    color = 'green'
  page = "<html><head><script>"
  page = page + "setTimeout(function(){location = ''},60000)"
  page = page + "</script></head>"
  page = page + "<body style='background-color: " + color + ";'>"
  page = page + "<p style='font-size: 96px; font-size: 20vw;"
  page = page + " margin: 20px; font-family: sans-serif'>"
  status = "Occupied"
  if isAvailable == True:
    status = "Available"
  page = page + status + "</p>"
  page = page + "</body></html>"
  statusPage.write(page)
  statusPage.close()
  return;

def parseBuffer(serialBuffer, lastMotion):
  if serialBuffer.find("|") == -1:
    print serialBuffer
    return lastMotion
  parsedPacket = parsePacket(serialBuffer)
  if parsedPacket != False:
    if parsedPacket['sensorType'] == 'MTN':
      if parsedPacket['sensorID'] == 'ConfRoom':
        if parsedPacket['payload'] == "Motion":
          lastMotion = time.time()
          if motionDetected == False:
            motionDetected = True
            setStatus(False)
  return lastMotion

print "\nCtrl-C to close COM port and exit.\n"

try:
  while (1):
    if motionDetected == True:
      if lastMotion < (time.time() - availableDelay):
        setStatus(True)
        motionDetected = False
    
    readLetter = serialPort.read() 
    
    if readLetter == "\n":
      lastMotion = parseBuffer(serialBuffer, lastMotion)
      serialBuffer = ""

    else:
      serialBuffer += readLetter

    time.sleep(0.05)
except KeyboardInterrupt:
  print "\nClosing COM port and exiting.\n"

serialPort.close()
