#include "exampleSetup.h"

int pin_LED_POWER = 13; 
int pin_ANTENNA_POWER = 10;
int pin_BUTTON = 2;
int buttonState = 1;

void setup() {  
  pinMode(pin_LED_POWER, OUTPUT);
  pinMode(pin_ANTENNA_POWER, OUTPUT);
  exampleSetup(); 
}

void loop() {
  if (digitalRead(pin_BUTTON) != buttonState) {
    if (buttonState == 1) {
      buttonState = 0;
      transmitString((char*) "Button Event: Button Pressed");
    } else {
      buttonState = 1;
    }
  }
  
  delay(50);
}

void transmitString(char* transmission) {
  digitalWrite(pin_LED_POWER, HIGH);
  digitalWrite (pin_ANTENNA_POWER, HIGH);
  
  vw_send((uint8_t *)transmission, strlen(transmission));
  vw_wait_tx();
  
  digitalWrite (pin_ANTENNA_POWER, LOW);
  digitalWrite(pin_LED_POWER, LOW); 
}
