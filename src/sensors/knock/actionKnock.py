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

def sendSlackWebHook(message):
  # https://api.slack.com/incoming-webhooks
  httpRequest = httplib.HTTPConnection("https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX", 80)
  httpRequest.connect()
  parameters = urllib.urlencode({'channel': 'general', 'text': message, 'username': 'Delivery Door', 'icon_emoji': ':door:'})
  headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
  httpRequest.request('POST', '/text', parameters, headers);
  response = httpRequest.getresponse()
  print response.read() + "\n"
  httpRequest.close()

def parseBuffer(serialBuffer):
  if serialBuffer.find("|") == -1:
    print serialBuffer
    return lastTextTime
  parsedPacket = parsePacket(serialBuffer)
  if parsedPacket != False:
    if parsedPacket['sensorType'] == 'KNC':
      if parsedPacket['sensorID'] == '1':
        if parsedPacket['payload'] == "Knocked":
          sendSlackWebHook("Someone just knocked at the delivery door. @channel")

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
