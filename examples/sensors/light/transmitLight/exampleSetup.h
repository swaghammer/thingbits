#include "VirtualWire.h"

float getPinAverage (byte pin, unsigned int sampleSize) { 
  long total; 
  total = 0; 
  for (int i = 0; i < sampleSize; i++) { 
    total = total + analogRead(pin);
  }
  return float(float(total) / float(sampleSize));
} 

int getBatteryVoltage() {
  float averageVoltage = getPinAverage(6, 5);
  
  return averageVoltage;
}

void checkBattery() {
  delay(20);
  int batteryVoltage;
  batteryVoltage = getBatteryVoltage();

  while (batteryVoltage < 181) {
    digitalWrite(13, HIGH);
    delay(90);
    digitalWrite(13, LOW);
    delay(150);
    digitalWrite(13, HIGH);
    delay(50);
    digitalWrite(13, LOW);
    delay(2000);
    
    batteryVoltage = getBatteryVoltage();
  }
  
}

void exampleSetup() {
  checkBattery();
  vw_set_tx_pin(11); 
  vw_set_ptt_pin(0);
  vw_setup(4800);
}




