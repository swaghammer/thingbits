char* sensorType = "THR";
char* myID = "1";
int heartbeatInterval = 3600; // seconds
int periodicReadingInterval = 600; // seconds, 0 for no periodic reading

#include "initialize.h"

void setup() {
  initializeSensor();
}

void loop() {
  sleepUntilEvent();

  processEvent();
}

void processEvent() {
  int pinThermometer = 0;
  char units[6] = "F";
  char message[14]; 
  dtoa(readTemp(pinThermometer), message, 0);
  strcat(message, units);
  
  sendPeriodic(message);
}
