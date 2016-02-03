from serial import *
import serial.tools.list_ports
from time import sleep, clock
import tweepy # http://nodotcom.org/python-twitter-tutorial.html

cfg = { 
  "consumer_key"        : "VALUE",
  "consumer_secret"     : "VALUE",
  "access_token"        : "VALUE",
  "access_token_secret" : "VALUE" 
  }
auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
api = tweepy.API(auth)

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
lastTweet = -1800
exercising = False

def parseBuffer(serialBuffer):
  if serialBuffer.find("Knock Event:") != -1:
    knockEvent = serialBuffer.split("Knock Event:")[1].strip()
    if knockEvent == "Exercise equipment was moved":
      return True
      
  return False

print "\nCtrl-C to close COM port and exit.\n"

try:
  while (1):
    readLetter = serialPort.read() 
    
    if readLetter == "\n":
      print serialBuffer
      exercising = parseBuffer(serialBuffer)
      serialBuffer = ""
    else:
      serialBuffer += readLetter
      
    if clock() > (lastTweet + (30 * 60)) and exercising == True:
      api.update_status("I'm exercising!")
      print "Tweeted: " + tweet
      lastTweet = clock()
      
    exercising = False  
    sleep(0.05)

except KeyboardInterrupt:
  print "\nClosing COM port and exiting.\n"

serialPort.close()
