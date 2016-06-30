char* sensorType = "TLT";
char* myID = "Garage";
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
  int pinTilt = 2;
  
  if (digitalRead(pinTilt) == HIGH) {
    sendEvent("Tilt down");
  }
  
  if (digitalRead(pinTilt) == LOW) {
    sendEvent("Tilt up");
  }
}
