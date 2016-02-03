#include "exampleSetup.h"

int pin_LED_POWER = 13; 
int pin_ANTENNA_POWER = 10;
int pin_KNOCK = 2;
int knockState = 1;

void setup() {  
  pinMode(pin_LED_POWER, OUTPUT);
  pinMode(pin_ANTENNA_POWER, OUTPUT);
  exampleSetup();
}

void loop() {
  if (digitalRead(pin_KNOCK) != knockState) {
    if (knockState == 1) {
      knockState = 0;
      transmitString((char*) "Knock Event: Exercise equipment was moved");
    } else {
      knockState = 1;
    }
  }
  
  delay(200);
} 

void transmitString(char* transmission) {
  digitalWrite(pin_LED_POWER, HIGH);
  digitalWrite (pin_ANTENNA_POWER, HIGH);
  
  vw_send((uint8_t *)transmission, strlen(transmission));
  vw_wait_tx();
  
  digitalWrite (pin_ANTENNA_POWER, LOW);
  digitalWrite(pin_LED_POWER, LOW); 
}
