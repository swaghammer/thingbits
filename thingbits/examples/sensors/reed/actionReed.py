import httplib, urllib
from serial import *
import serial.tools.list_ports
from time import clock, sleep

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

def setStatus(isOpen):
  fileName = "doorState.html"
  statusPage = open(fileName, 'w')
  color = 'green'
  if isOpen == True:
    color = 'red'
  page = "<html><head><script>"
  page = page + "setTimeout(function(){location = ''},60000)"
  page = page + "</script></head>"
  page = page + "<body style='background-color: " + color + ";'>"
  page = page + "<p style='font-size: 96px; font-size: 20vw;"
  page = page + " margin: 20px; font-family: sans-serif'>"
  status = "CLOSED"
  if isOpen == True:
    status = "OPEN"
  page = page + status + "</p>"
  page = page + "</body></html>"
  statusPage.write(page)
  statusPage.close()
  return

def parseBuffer(serialBuffer):
  if serialBuffer.find("|") == -1:
    print serialBuffer
    return
  parsedPacket = parsePacket(serialBuffer)
  if parsedPacket != False:
    if parsedPacket['sensorType'] == 'RED':
      if parsedPacket['sensorID'] == '1':
        print time.strftime("%Y-%m-%d %H:%M:%S|") + serialBuffer.strip()
        if parsedPacket['messageType'] == 'P':
          if parsedPacket['payload'] == "Is Open":
            setStatus(True)
          if parsedPacket['payload'] == "Is Closed":
            setStatus(False)
        if parsedPacket['messageType'] == 'E':
          if parsedPacket['payload'] == "Opened":
            sendText(phoneNumber, "The back door just opened")
            
print "\nCtrl-C to close COM port and exit.\n"

try:
  while (1):
    readLetter = serialPort.read() 
    
    if readLetter == "\n":
      parseBuffer(serialBuffer)
      serialBuffer = ""

    else:
      serialBuffer += readLetter

    sleep(0.05)
except KeyboardInterrupt:
  print "\nClosing COM port and exiting.\n"

serialPort.close()

