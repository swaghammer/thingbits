#include "exampleSetup.h"

int pin_LED_POWER = 13; 
int pin_ANTENNA_POWER = 10;
int pin_MOTION = 2;
int lastMotion = 0;

void setup() {  
  pinMode(pin_LED_POWER, OUTPUT);
  pinMode(pin_ANTENNA_POWER, OUTPUT);
  exampleSetup();
}

void loop() {
  int motionRead = digitalRead(pin_MOTION);
  if (lastMotion != motionRead) {
    if (lastMotion == 0) {
      transmitString((char*) "Motion Event: Motion Detected");
    }
    lastMotion = motionRead;
  }
  
  delay(500);
} 

void transmitString(char* transmission) {
  digitalWrite(pin_LED_POWER, HIGH);
  digitalWrite (pin_ANTENNA_POWER, HIGH);
  
  vw_send((uint8_t *)transmission, strlen(transmission));
  vw_wait_tx();
  
  digitalWrite (pin_ANTENNA_POWER, LOW);
  digitalWrite(pin_LED_POWER, LOW); 
}
