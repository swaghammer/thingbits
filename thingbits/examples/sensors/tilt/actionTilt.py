import httplib, urllib
from serial import *
import serial.tools.list_ports
from time import clock, sleep

modeSelect = input("Select messaging mode\n1 - When garagedoor is open too long\n2 - Every time it opens or closes\n")
mode = "tiltWasOpenTooLong"
if modeSelect == 2:
  mode = "everyTilt"

phoneNumber = input("\nWhat phone number should receive the texts? (ex. 5551234567)\n")

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
openSince = 0
openTooLong = (5 * 60) # five minutes

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

def sendText(number, message):
  httpRequest = httplib.HTTPConnection("textbelt.com", 80)
  httpRequest.connect()
  parameters = urllib.urlencode({'number': number, 'message': message})
  headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
  httpRequest.request('POST', '/text', parameters, headers);
  response = httpRequest.getresponse()
  print response.read() + "\n"
  httpRequest.close()

def checkOpenTooLong(openSince):
  if openSince > 0 and (clock() - openSince) > (openTooLong):
    alert = "Garage door has been open too long"
    print "Sending text: " + alert
    sendText(phoneNumber, alert)
    openSince = clock()
  return openSince

def parseBuffer(serialBuffer, openSince):
  if serialBuffer.find("|") == -1:
    print serialBuffer
    return
  parsedPacket = parsePacket(serialBuffer)
  if parsedPacket != False:
    if parsedPacket['sensorType'] == 'TLT':
      if parsedPacket['sensorID'] == '1':
        print time.strftime("%Y-%m-%d %H:%M:%S|") + serialBuffer.strip()
        if mode == "everyTilt":
          if parsedPacket['payload'] == "Tilt up":
            sendText(phoneNumber, "Garage door is open")
          else:
            sendText(phoneNumber, "Garage door is closed")
        if mode == "tiltWasOpenTooLong":
          if parsedPacket['payload'] == "Tilt up":
            if openSince == 0:
              openSince = clock()
          else:
            openSince = 0
  return openSince

print "\nCtrl-C to close COM port and exit.\n"

try:
  while (1):
    if mode == "tiltWasOpenTooLong" and openSince > 0 and (clock() - openSince) > (openTooLong):
      openSince = checkForOpenTooLong(openSince, openTooLong)
        
    readLetter = serialPort.read() 
    
    if readLetter == "\n":
      print serialBuffer
      openSince = parseBuffer(serialBuffer, openSince)
      serialBuffer = ""

    else:
      serialBuffer += readLetter

    sleep(0.05)
except KeyboardInterrupt:
  print "\nClosing COM port and exiting.\n"

serialPort.close()

