#include "exampleSetup.h"

int pin_LED_POWER = 13; 
int pin_ANTENNA_POWER = 10;
int pin_BUTTON_ONE = 2;
int pin_BUTTON_TWO = 3;
int buttonOneState = 1;
int buttonTwoState = 1;

void setup() {  
  pinMode(pin_LED_POWER, OUTPUT);
  pinMode(pin_ANTENNA_POWER, OUTPUT);
  exampleSetup();
}

void loop() {
  if (digitalRead(pin_BUTTON_ONE) != buttonOneState) {
    if (buttonOneState == 1) {
      buttonOneState = 0;
      transmitString((char*) "Button Event: Car Entered");
    } else {
      buttonOneState = 1;
    }
  }
  
  if (digitalRead(pin_BUTTON_TWO) != buttonTwoState) {
    if (buttonTwoState == 1) {
      buttonTwoState = 0;
      transmitString((char*) "Button Event: Car Exited");
    } else {
      buttonTwoState = 1;
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
