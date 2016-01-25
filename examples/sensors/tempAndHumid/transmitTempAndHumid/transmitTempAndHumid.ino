#include "exampleSetup.h"

int pin_LED_POWER = 13; 
int pin_ANTENNA_POWER = 10;
int pin_THERMOMETER = A0;
int pin_HUMIDITY = A0;

void setup() {  
  pinMode(pin_LED_POWER, OUTPUT);
  pinMode(pin_ANTENNA_POWER, OUTPUT);
  exampleSetup();
}

void loop() {
  float averageReading = 0.0;
  for (int i = 0; i < 10; i++) {
    averageReading = averageReading + (((float(analogRead(pin_THERMOMETER)) * 0.2978515625) - 50.0) / 10.0);
  }

  char message[22] = "Temperature Reading: ";
  char temperature[10];
  itoa(averageReading, temperature, 10);

  transmitString((char*) strcat(message, temperature));

  delay(1000);

  message = "Humidity Reading: ";
  char humidity[10];
  itoa(analogRead(pin_HUMIDITY), humidity, 10);

  transmitString((char*) strcat(message, humidity));
  
  delay(4000);
} 

void transmitString(char* transmission) {
  digitalWrite(pin_LED_POWER, HIGH);
  digitalWrite (pin_ANTENNA_POWER, HIGH);
  
  vw_send((uint8_t *)transmission, strlen(transmission));
  vw_wait_tx();
  
  digitalWrite (pin_ANTENNA_POWER, LOW);
  digitalWrite(pin_LED_POWER, LOW); 
}
