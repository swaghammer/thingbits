char* sensorType = "TMP";
char* myID = "BOSS";
int heartbeatInterval = 3600; // seconds
int periodicReadingInterval = 600; // seconds, 0 for no periodic reading
float CalVal= -1.25; //calibration offset value 

#include "initialize.h"

void setup() {
  initializeSensor();
  processEvent();
}

void loop() {
  sleepUntilEvent();

  processEvent();
}

void processEvent() {
  int pinThermometer = 0;
  char units[6] = "F";
  char message[14]; 
  float Temp=readTemp(pinThermometer)+CalVal;
  dtoa(Temp, message, 0);
  strcat(message, units);
  
  sendPeriodic(message);
}
