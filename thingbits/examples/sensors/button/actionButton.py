import httplib, urllib
from serial import *
import serial.tools.list_ports
from time import time, sleep

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
textDelay = 90; # seconds
lastTextTime = time() - textDelay;

def sendText(number, message):
  httpRequest = httplib.HTTPConnection("textbelt.com", 80)
  httpRequest.connect()
  parameters = urllib.urlencode({'number': number, 'message': message})
  headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
  httpRequest.request('POST', '/text', parameters, headers);
  response = httpRequest.getresponse()
  print response.read() + "\n"
  httpRequest.close()

def parseBuffer(serialBuffer, lastTextTime, textDelay):
  if serialBuffer.find("Button Event:") != -1:
    buttonEvent = serialBuffer.split("Button Event:")[1].strip()
    if buttonEvent == "Button Pressed":
      if time() > (lastTextTime + textDelay):
        lastTextTime = time()
        print "The button was pressed. And a text is being sent.\n"
        sendText(phoneNumber, "The button was pressed")
      else:
        print "The button was pressed. But it's too soon to send another text.\n"
  return lastTextTime

print "\nCtrl-C to close COM port and exit.\n"

try:
  while (1):
    readLetter = serialPort.read() 
    
    if readLetter == "\n":
      print serialBuffer
      lastTextTime = parseBuffer(serialBuffer, lastTextTime, textDelay)
      serialBuffer = ""

    else:
      serialBuffer += readLetter

    sleep(0.05)
except KeyboardInterrupt:
  print "\nClosing COM port and exiting.\n"

serialPort.close()
