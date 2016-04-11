char* sensorType = "BCN";
char* myID = "Pinger";
int heartbeatInterval = 8; // seconds
int periodicReadingInterval = 0; // seconds, 0 for no periodic readings

#include "initialize.h"

void setup() {
  initializeSensor();
}

void loop() {
  sleepUntilEvent();
}

