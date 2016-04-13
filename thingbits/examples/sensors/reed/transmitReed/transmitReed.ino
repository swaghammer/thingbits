char* sensorType = "RED";
char* myID = "1";
int heartbeatInterval = 3600; // seconds
int periodicReadingInterval = 120; // seconds, 0 for no periodic reading

#include "initialize.h"

void setup() {
  initializeSensor();
}

void loop() {
  sleepUntilEvent();

  processEvent();
}

void processEvent() {
  int pinReed = 2;

  if (periodicReading) {
    if (digitalRead(pinReed) == HIGH) {
      sendPeriodic("Is Open");
    } else {
      sendPeriodic("Is Closed");
    }
    return;
  } else {
    if (digitalRead(pinReed) == HIGH) {
      sendEvent("Opened");
    }
  }
}
