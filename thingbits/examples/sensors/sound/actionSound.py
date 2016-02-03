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

def sendSlackWebHook(message):
  # https://api.slack.com/incoming-webhooks
  httpRequest = httplib.HTTPConnection("https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX", 80)
  httpRequest.connect()
  parameters = urllib.urlencode({'channel': 'baby-monitor', 'text': message, 'username': 'baby', 'icon_emoji': ':baby:'})
  headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
  httpRequest.request('POST', '/text', parameters, headers);
  response = httpRequest.getresponse()
  print response.read() + "\n"
  httpRequest.close()
  
def parseBuffer(serialBuffer):
  if serialBuffer.find("Volume Reading:") != -1:
    babyVolume = int(serialBuffer.split("Volume Reading:")[1].strip())

    if babyVolume > 200 and babyVolume <= 500:
      sendSlackWebHook("goo goo ga ga")
    else if babyVolume > 500 and babyVolume <= 800:
      sendSlackWebHook("waaa waaa")
    else if babyVolume > 800:
      sendSlackWebHook("WHAAAA!!! WWHAAAA!!")
      
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
