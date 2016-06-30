char* sensorType = "MST";
char* myID = "1";
int heartbeatInterval = 3600; // seconds
int periodicReadingInterval = (4 * 60 * 60); // seconds, 0 for no periodic reading

#include "initialize.h"

void setup() {
  initializeSensor();
}

void loop() {
  sleepUntilEvent();

  processEvent();
}

void processEvent() {
  int pinMoisture = 0; 
  double percentMoist = double((1024 - analogRead(pinMoisture)) / 10);
  if (percentMoist < 0) {
    percentMoist = 0;
  } else if (percentMoist > 100) {
    percentMoist = 100;
  }
  char message[14]; 
  dtoa(percentMoist, message, 0);
  
  sendPeriodic(message);
}
