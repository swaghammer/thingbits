#include "VirtualWire.h"

int pin_LED_POWER = 13;
int pin_SIGNAL_STRENGTH = 7;

void setup() {
  pinMode(pin_LED_POWER, OUTPUT);
  digitalWrite(pin_LED_POWER,LOW);
  
  vw_setup(4800);
  vw_rx_start();
  
  Serial.begin(57600);
  Serial.println("* Example receiver setup complete");
} 

void loop() {
  uint8_t readBuffer[VW_MAX_MESSAGE_LEN];
  uint8_t bufferLength = VW_MAX_MESSAGE_LEN;
  
  if (vw_have_message()) {
    Serial.print(getSignalStrength());
    Serial.print("%~");
    
    digitalWrite(pin_LED_POWER, HIGH);
    
    vw_get_message(readBuffer, &bufferLength);

    for (int i = 0; i < bufferLength; i++) {
      Serial.print(char(readBuffer[i])); 
    }
    Serial.println("");
    
    digitalWrite(pin_LED_POWER,LOW);
  }
}

int getSignalStrength() {
  int rawSignalStrenth = analogRead(pin_SIGNAL_STRENGTH);
  if (rawSignalStrenth < 151) {
    return 0;
  }
  if (rawSignalStrenth > 399) {
    return 100;
  }

  return int(floor(float(rawSignalStrenth - 150) / 2.5));
}

