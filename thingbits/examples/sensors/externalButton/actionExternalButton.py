import httplib, urllib
from serial import *
import serial.tools.list_ports
import time

phoneNumber = input("\nWhat phone number should receive the texts? (ex. 5551234567)\n")

ports = sorted(serial.tools.list_ports.comports())
i = 1
for elem in ports:
  print i, " - " + elem[0]
  i = i + 1
selectedPort = input("Select COM port option: ")
comPort = ports[selectedPort - 1][0]

serialPort = Serial(comPort, 57600, timeout=0, writeTimeout=0)
serialBuffer = ""
consecutiveOpen = 0

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

def sendText(number, message):
  httpRequest = httplib.HTTPConnection("textbelt.com", 80)
  httpRequest.connect()
  parameters = urllib.urlencode({'number': number, 'message': message})
  headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
  httpRequest.request('POST', '/text', parameters, headers);
  response = httpRequest.getresponse()
  print response.read() + "\n"
  httpRequest.close()

def parseBuffer(serialBuffer, consecutiveOpen):
  if serialBuffer.find("|") == -1:
    print serialBuffer
    return consecutiveOpen
  parsedPacket = parsePacket(serialBuffer)
  if parsedPacket != False:
    if parsedPacket['sensorType'] == 'EXT':
      if parsedPacket['sensorID'] == 'Fridge':
        if parsedPacket['payload'] == "Open":
          consecutiveOpen = consecutiveOpen + 1
          if consecutiveOpen > 3:
            sendText(phoneNumber, "The fridge has been open for " + consecutiveOpen + " consectutive minutes")
        else:
          consecutiveOpen = 0
  return consecutiveOpen
        
print "\nCtrl-C to close COM port and exit.\n"

try:
  while (1):
    readLetter = serialPort.read() 
    
    if readLetter == "\n":
      consecutiveOpen = parseBuffer(serialBuffer, consecutiveOpen)
      serialBuffer = ""

    else:
      serialBuffer += readLetter

    time.sleep(0.05)
except KeyboardInterrupt:
  print "\nClosing COM port and exiting.\n"

serialPort.close()
