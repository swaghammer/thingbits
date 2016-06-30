char* sensorType = "SND";
char* myID = "Ninja";
int heartbeatInterval = 3600; // seconds
int periodicReadingInterval = 0; // seconds, 0 for no periodic reading

#include "initialize.h"

void setup() {
  initializeSensor();
}

void loop() {
  sleepUntilEvent();

  processEvent();
}

void processEvent() {
  int pinSound = 2;
  
  if (digitalRead(pinSound) == LOW) {
    sendEvent("Sound");
  }
}
