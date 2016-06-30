char* sensorType = "LIT";
char* myID = "Solar";
int heartbeatInterval = 3600; // seconds
int periodicReadingInterval = (10 * 60); // seconds, 0 for no periodic reading

#include "initialize.h"

void setup() {
  initializeSensor();
}

void loop() {
  sleepUntilEvent();

  processEvent();
}

void processEvent() {
  int pinLight = 0;
  double reading = floor(((double) digitalRead(pinLight))  / 10.2);
  char readingString[3];
  dtoa((double) reading, readingString, 0);
  sendPeriodic(readingString);
}

