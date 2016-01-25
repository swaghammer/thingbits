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
lastText = 0

def sendText(number, message):
  httpRequest = httplib.HTTPConnection("textbelt.com", 80)
  httpRequest.connect()
  parameters = urllib.urlencode({'number': number, 'message': message})
  headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
  httpRequest.request('POST', '/text', parameters, headers);
  response = httpRequest.getresponse()
  print response.read() + "\n"
  httpRequest.close()
  
def parseBuffer(serialBuffer, lastText):
  if serialBuffer.find("Vibration Reading:") != -1:
    vibration = int(serialBuffer.split("Vibration Reading:")[1].strip())
    if (time.clock() - 60) < lastText or vibration <= 200:
      return lastText
    lastText = time.clock()
    if vibration <= 500:
      sendText(phoneNumber, "The cat is messing with your house plant")
    else if vibration > 500 and vibration <= 800:
      sendText(phoneNumber, "The cat is shaking your plant a whole lot")
    else if vibration > 800:
      sendText(phoneNumber, "The cat has declared war on your plant")
    return lastText
      
print "\nCtrl-C to close COM port and exit.\n"

try:
  while (1):
    readLetter = serialPort.read() 
    
    if readLetter == "\n":
      print serialBuffer
      lastText = parseBuffer(serialBuffer, lastText)
      serialBuffer = ""

    else:
      serialBuffer += readLetter

    time.sleep(0.05)
except KeyboardInterrupt:
  print "\nClosing COM port and exiting.\n"

serialPort.close()
