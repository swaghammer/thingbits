#if (ARDUINO < 100)
#include "WProgram.h"
#else
#include "Arduino.h"
#endif
#include <string.h>
#include <math.h>
#include <avr/interrupt.h>
#include <avr/pgmspace.h>
#include <avr/power.h>
#include <avr/sleep.h>
#include <avr/wdt.h>

#ifndef cbi
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif
#ifndef sbi
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))
#endif

#include "VirtualWire.h"

const int Aref = 3050;
const float ANAscale = float(Aref) / 1024.0;
const byte pin_BV = 6;
const byte pin_TXDen = 9;
const byte pin_ANTENNA_POWER = 10;
const byte pin_TXD = 11;
const byte pin_LED = 13; 
const byte pinButton = 2;

volatile int periodicCountdown, periodicReset;
volatile int heartbeatCountdown, heartbeatReset; 
volatile byte wakeWhy = 0; 
char sSBName[15];
char sTXID[6]; 
double dBV;
char sBV[6]; 
byte bSBN;
byte debugON;
byte D2stat, D3stat, HL;

char *dtoa(double dnum, char *mja, int prec) { 
  char *ret = mja; 
  long pm = 1; 
  byte wp = prec;
  while (wp > 0) { 
    pm = pm*10;  
    wp--;  
  }
  long Lodp = long(dnum); 
  double diff = (dnum - double(Lodp))* double(pm); 
  if (dnum >= 0) {
    diff = (diff + 0.5);  
  } else { 
    diff = (diff - 0.5); 
  }
  long Rodp = abs(long(diff));  
  Lodp = abs(Lodp);  
  if (Rodp == pm) { 
    Lodp = Lodp + 1;  
    Rodp = 0;  
  }
  if ((dnum < 0) & ((Rodp + Lodp) > 0)) { 
    *mja++ = '-';  
  } 
  ltoa(Lodp, mja, 10);
  if (prec > 0) { 
    while (*mja != '\0') { 
      mja++; 
    } 
    *mja++ = '.'; 
    pm=10; 
    while (prec > 1) { 
      if (Rodp < pm) { 
        *mja='0'; 
        mja++; 
      } 
      pm=pm*10;  
      prec--; 
    }
    ltoa(Rodp, mja, 10); 
  }  
  return ret; 
} 

float readPinAverage (byte pinNumber, unsigned int sampleCount) { 
  long sumTotal; 
  sumTotal = 0; 
  for (int i = 0; i < sampleCount; i++) { 
    sumTotal = sumTotal + analogRead(pinNumber); 
  }
  float averageReading = float(float(sumTotal) / float(sampleCount)); 
  return averageReading; 
}

float readBatteryVoltage() {
  float fBV = readPinAverage(pin_BV, 5);
  fBV = (fBV* ANAscale) / 500.0; 
  return fBV; 
} 

byte makeCheckSumByte(char* transmission, int transmissionLength) {
  byte checkSumByte = 0;
  for (int i = 0; i < transmissionLength; i++) {
    checkSumByte = checkSumByte ^ transmission[i];
  }
  if (checkSumByte == 0) {
    checkSumByte = 1;
  }
  return checkSumByte;
}

void transmitString(char* transmission) {
  int transmissionLength = strlen(transmission);

  char checkSumByte = makeCheckSumByte(transmission, transmissionLength);
  char cleanTransmission[40];
  *cleanTransmission = 0; 
  for (int i = 0; i < transmissionLength; i++) {
    cleanTransmission[i] = transmission[i];
  }
  cleanTransmission[transmissionLength] = checkSumByte;
  cleanTransmission[transmissionLength + 1] = 0;

  digitalWrite(pin_LED, HIGH);
  digitalWrite(pin_ANTENNA_POWER, HIGH);
  
  vw_send((uint8_t *)cleanTransmission, (transmissionLength + 1)); 
  vw_wait_tx();
  
  dBV = readBatteryVoltage(); 
  digitalWrite(pin_ANTENNA_POWER, LOW); 
  digitalWrite(pin_LED, LOW); 
}

char* msgTooLong = "<--Msg too long. Max 31 char-->";

void sendMessage(char* messageType, char* message) {
  dtoa(dBV, sBV, 1); 
  if ((strlen(sensorType) + 
      strlen(myID) + 
      strlen(messageType) + 
      strlen(sBV) + 
      strlen(message) + 
      + 5) > 32) {
    transmitString(msgTooLong);
    return;
  }
  
  char transmissionString[40];
  *transmissionString = 0; 
  strcat(transmissionString, sensorType);
  strcat(transmissionString, "|");
  strcat(transmissionString, myID);
  strcat(transmissionString, "|");
  strcat(transmissionString, messageType);
  strcat(transmissionString, "|");
  strcat(transmissionString, sBV);
  if (strlen(message) > 0) {
    strcat(transmissionString, "|");
    strcat(transmissionString, message);
  }

  transmitString(transmissionString);
}

void sendEvent(char* message) {
  sendMessage("E", message);
}

void sendInfo(char* message) {
  sendMessage("I", message);  
}

void sendPeriodic(char* message) {
  sendMessage("P", message);  
}

double readTemp(byte pinNumber) { 
  digitalWrite(pin_ANTENNA_POWER, HIGH); 
  delay(5);
  double MF = double(double(readPinAverage(pinNumber, 10)) * double(ANAscale));
  MF = double((MF - 500.0) / 10.0);  
  digitalWrite(pin_ANTENNA_POWER, LOW); 

  return double((MF * 1.8) + 32.0);
} 

void Send_ANA (byte port) {
  float fVal;
  char sVal[6];
  // DoMsgHeader(sWhy);
  // strcat(sMsg, "|");
  itoa(port, sVal, 10);
  // strcat(sMsg, sVal);
  // strcat(sMsg, "=");
  fVal = readPinAverage(port, 30);
  fVal = (fVal* ANAscale) / 1000.0;
  dtoa(fVal, sVal, 3);
  // strcat(sMsg, sVal);
  // strcat_P(sMsg, (char*)pgm_read_word(&(table_PMS[2]))); //Volts
  // XMIT_STRING(sMsg, strlen(sMsg), 50);
}

void checkBatteryVoltage() {
  if (dBV < 2.8) {
    sendInfo("Low Battery");
  }
}
  
bool buttonPushed;
bool buttonReleased;
bool tiltHorizontal;
bool tiltVertical;
bool periodicReading;

void detachInterrupts() {
  detachInterrupt(digitalPinToInterrupt(2));
  // detachInterrupt(digitalPinToInterrupt(3));
}

void digital2Change() {  
  sleep_disable(); 
  detachInterrupts();
  
  if (digitalRead(2) == LOW) {
    wakeWhy = 2;
    buttonPushed = true;
    tiltHorizontal = true;
  } else {
    wakeWhy = 3;
    buttonReleased = true;
    tiltVertical = true;
  }
}

void digital3Change() {  
  sleep_disable(); 
  detachInterrupts();

  if (digitalRead(3) == LOW) {
    wakeWhy = 5;
  } else {
    wakeWhy = 6;
  }
}

void attachInterrupts() {
  attachInterrupt(digitalPinToInterrupt(2), digital2Change, CHANGE);
  // attachInterrupt(digitalPinToInterrupt(3), digital3Change, CHANGE);
}

void clearEventFlags() {
  buttonPushed = false;
  buttonReleased = false;
  tiltHorizontal = false;
  tiltVertical = false;
  periodicReading = false;
}

ISR(WDT_vect) { 
  sleep_disable(); 
  detachInterrupts();
  
  wakeWhy = 0; 

  if (periodicReset > 0) {
    periodicCountdown--; 
    if (periodicCountdown < 1) {
      periodicCountdown = periodicReset; 
      wakeWhy = 1;
      periodicReading = true;
    }
  }

  heartbeatCountdown--;
  if (heartbeatCountdown < 1) {
    heartbeatCountdown = heartbeatReset; 
    wakeWhy = 4;
  } 
   
}

void sleepUntilEvent() {
  bool keepSleeping = true;

  do {
    checkBatteryVoltage();

    clearEventFlags();

    wakeWhy = 0;
    while (
      (periodicReset > 0 ? (periodicCountdown > 0) : true) && 
      heartbeatCountdown > 0 && 
      wakeWhy == 0) {

      sleep_enable();  
      attachInterrupts();
      set_sleep_mode(SLEEP_MODE_PWR_DOWN);  
      cli(); 
      sei(); 
      
      sleep_mode(); //Z-Z-Z-Z-Z-Z-Z-Z-Z-Z-Z-Z-Z-Z-Z-Z-Z-Z-Z
      
      sleep_disable(); 
    }

    switch (wakeWhy) {
      case 0: break;
      case 1: keepSleeping = false; break; // periodic reading
      case 2: keepSleeping = false; break; // D2 low
      case 3: keepSleeping = false; break; // D2 high
      case 4: sendMessage("I", "Heartbeat"); break;
      case 5: keepSleeping = false; break; // D3 low
      case 6: keepSleeping = false; break; // D3 high
      default: break; 
    }

  } while (keepSleeping);
}

void initializeSensor() {
  cli(); 
  wdt_reset(); 
  WDTCSR |= B00011000; 
  WDTCSR = B01100001; 
  sei(); 
  analogReference(DEFAULT); 

  detachInterrupts();

  digitalWrite(pin_LED, LOW); 
  pinMode(pin_LED, OUTPUT);
  digitalWrite(pin_ANTENNA_POWER, LOW); 
  pinMode(pin_ANTENNA_POWER, OUTPUT);
  for (int pn = 2; pn < pin_ANTENNA_POWER; pn++) {
    pinMode(pn, INPUT); 
    digitalWrite(pn, HIGH); 
  }  
  vw_set_tx_pin(pin_TXD);  
  vw_set_ptt_pin(0); 
  vw_setup(4800); 

  digitalWrite(pin_ANTENNA_POWER, HIGH); 
  vw_send((uint8_t *)0, 0); 
  vw_wait_tx();
  dBV = readBatteryVoltage(); 
  digitalWrite(pin_ANTENNA_POWER, LOW); 

  heartbeatReset = 1;
  if (floor(float(heartbeatInterval) / 8.0) > 1.0) {
    heartbeatReset = int(floor(float(heartbeatInterval) / 8.0));
  }
  heartbeatCountdown = heartbeatReset; 

  periodicReset = 0;
  if (periodicReadingInterval > 0) {
    periodicReset = 1;
    if (floor(float(periodicReadingInterval) / 8.0) > 1.0) {
      periodicReset = int(floor(float(periodicReadingInterval) / 8.0));
    }
  }
  periodicCountdown = periodicReset;
  
  digitalWrite(2, LOW); 
      
  sendMessage("I", "Initialized");
}


