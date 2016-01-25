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
totalParkingSpots = 10
filledSpots = 0
lastTweet = -3600

def getTweet(filledSpots, totalSpots):
  if filledSpots < 1:
    return "The lot's empty. C'mon down!"
  if filledSpots < (totalSpots / 2):
    return "Still plenty of space in our parking lot."
  if filledSpots < totalSpots:
    return "Space is running out. You'd better hurry up!"
  return "Sorry, the lot is full at the moment"

def parseBuffer(serialBuffer, filledSpots):
  if serialBuffer.find("Button Event:") != -1:
    buttonEvent = serialBuffer.split("Button Event:")[1].strip()
    if buttonEvent == "Car Entered":
      filledSpots = filledSpots + 1
    if buttonEvent == "Car Exited":
      filledSpots = filledSpots - 1
  return filledSpots

print "\nCtrl-C to close COM port and exit.\n"

try:
  while (1):
    if clock() > (lastTweet + (60 * 60)):
      tweet = getTweet(filledSpots, totalParkingSpots)
      api.update_status(tweet)
      print "Tweeted: " + tweet
      lastTweet = clock()
    
    readLetter = serialPort.read() 
    
    if readLetter == "\n":
      print serialBuffer
      filledSpots = parseBuffer(serialBuffer, filledSpots)
      print "Currently in the parking lot: " + str(filledSpots)
      serialBuffer = ""

    else:
      serialBuffer += readLetter

    sleep(0.05)
except KeyboardInterrupt:
  print "\nClosing COM port and exiting.\n"

serialPort.close()
