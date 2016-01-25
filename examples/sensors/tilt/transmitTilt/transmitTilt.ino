#include "exampleSetup.h"

int pin_LED_POWER = 13;
int pin_ANTENNA_POWER = 10;
int pin_TILT_SENSOR = 2;

int tiltState;
int tiltEstimate = 50;
int tiltCertaintyDelay = 1000; // milliseconds
int loopDelay;

void setup() {
  pinMode(pin_LED_POWER, OUTPUT);
  pinMode(pin_ANTENNA_POWER, OUTPUT);
  if (tiltCertaintyDelay < 100) {
    tiltCertaintyDelay = 100;
  }
  loopDelay = floor(tiltCertaintyDelay / 100);
  exampleSetup();
}

void loop() {
  if (digitalRead(pin_TILT_SENSOR)) {
    tiltEstimate++;
  } else {
    tiltEstimate--;
  }
  if (tiltEstimate > 100) {
    tiltEstimate = 100;
  }
  if (tiltEstimate < 0) {
    tiltEstimate = 0;
  }

  if (tiltState == 0 && tiltEstimate > 95) {
    transmitString((char*) "Tilt Event: Vertical");
    tiltState = 1;
  }
  
  if (tiltState == 1 && tiltEstimate < 5) {
    transmitString((char*) "Tilt Event: Horizontal");
    tiltState = 0;
  }
  
  delay(loopDelay);
}

void transmitString(char* transmission) {
  digitalWrite(pin_LED_POWER, HIGH);
  digitalWrite (pin_ANTENNA_POWER, HIGH);
  
  vw_send((uint8_t *)transmission, strlen(transmission));
  vw_wait_tx();
  
  digitalWrite (pin_ANTENNA_POWER, LOW);
  digitalWrite(pin_LED_POWER, LOW);
}
