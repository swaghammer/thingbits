char* sensorType = "MTN";
char* myID = "ConfRoom";
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
  int pinMotion = 2;
  
  if (digitalRead(pinMotion) == LOW) {
    sendEvent("Motion");
  }
}
