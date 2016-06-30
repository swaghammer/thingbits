char* sensorType = "BTN";
char* myID = "1";
int heartbeatInterval = 3600; // seconds
int periodicReadingInterval = 0; // seconds, 0 for no periodic reading

#include "initialize.h"

void setup() {
  Serial.begin(57600);
  initializeSensor();
}

void loop() {
  // sleepUntilEvent();

  processEvent();
}

void processEvent() {
  int pinButton = 2;
  
  if (digitalRead(pinButton) == LOW) {
    Serial.print("D");
    //sendEvent("Pushed");
  } else {
    Serial.print("U");
  }

  delay(5);
}
