#include "exampleSetup.h"

int pin_LED_POWER = 13; 
int pin_ANTENNA_POWER = 10;
int pin_LIGHT = A0;

void setup() {  
  pinMode(pin_LED_POWER, OUTPUT);
  pinMode(pin_ANTENNA_POWER, OUTPUT);
  exampleSetup();
}

void loop() {
  char message[22] = "Light Reading: ";
  char brightness[9];
  itoa(analogRead(pin_LIGHT), brightness, 10);

  transmitString((char*) strcat(message, brightness));

  delay(2000);
} 

void transmitString(char* transmission) {
  digitalWrite(pin_LED_POWER, HIGH);
  digitalWrite (pin_ANTENNA_POWER, HIGH);
  
  vw_send((uint8_t *)transmission, strlen(transmission));
  vw_wait_tx();
  
  digitalWrite (pin_ANTENNA_POWER, LOW);
  digitalWrite(pin_LED_POWER, LOW); 
}
