char* sensorType = "EXT";
char* myID = "Fridge";
int heartbeatInterval = 3600; // seconds
int periodicReadingInterval = 60; // seconds, 0 for no periodic reading

#include "initialize.h"

void setup() {
  initializeSensor();
}

void loop() {
  sleepUntilEvent();

  processEvent();
}

void processEvent() {
  int pinDoor = 2;

  if (digitalRead(pinDoor) == HIGH) {
    sendEvent("Open");
  } else {
    sendEvent("Closed");
  }
}

