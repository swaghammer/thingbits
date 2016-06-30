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
tweetDelay = (30 * 60)
lastTweet = tweetDelay * -1
exercising = False

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

def parseBuffer(serialBuffer):
  if serialBuffer.find("|") == -1:
    print serialBuffer
    return False
  parsedPacket = parsePacket(serialBuffer)
  if parsedPacket != False:
    if parsedPacket['sensorType'] == 'SHK':
      if parsedPacket['sensorID'] == 'Exercise':
        if parsedPacket['payload'] == "Shake":
          return True
  return False

print "\nCtrl-C to close COM port and exit.\n"

try:
  while (1):
    readLetter = serialPort.read() 
    
    if readLetter == "\n":
      exercising = parseBuffer(serialBuffer)
      serialBuffer = ""
    else:
      serialBuffer += readLetter
      
    if clock() > (lastTweet + tweetDelay) and exercising == True:
      tweet = "I'm exercising!"
      api.update_status(tweet)
      print "Tweeted: " + tweet
      lastTweet = clock()
      
    exercising = False  
    sleep(0.05)

except KeyboardInterrupt:
  print "\nClosing COM port and exiting.\n"

serialPort.close()
