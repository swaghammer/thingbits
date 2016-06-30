char* sensorType = "BTN";
char* myID = "Simple";
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
  int pinButton = 2;
  
  if (digitalRead(pinButton) == LOW) {
    sendEvent("Pushed");
  }

  // sendEvent("Event!");
}
