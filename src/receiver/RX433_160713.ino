//Blame goes to...
//  Marlyn Anderson

#include "VirtualWire.h"
#include <EEPROM.h>

const int pin_LED_POWER = 13;
const int pin_RSS = 7;
const int EE_SysBits=1023; //System/Global flag bits are always at the top
byte SysBits;
const int EE_RssMax=SysBits-1;
const int EE_RssMin=EE_RssMax-1;
int RssMax,RssMin,RssNow;

//**** Strings go into program flash memory *****
const char Ver0[] PROGMEM = "* RX433_160713";
const char Ssr1[] PROGMEM = "* Signal Strength Reset Done.";
const char Max2[] PROGMEM = "* RssMax=";
const char Min3[] PROGMEM = " RssMin=";
PGM_P const table_RESP[] PROGMEM = {Ver0,Ssr1,Max2,Min3};

const char Hlp0[] PROGMEM = "* ver -> Version Date/Number of Firmware";
const char Hlp1[] PROGMEM = "* rssmm -> Reset Signal Strength Max/Min";
PGM_P const table_HELP[] PROGMEM = {Hlp0,Hlp1};
const byte HLPlim=2;

//*******************************************
//******** Main ****************************

void setup() {
  analogReference(EXTERNAL);
  pinMode(pin_LED_POWER, OUTPUT);
  digitalWrite(pin_LED_POWER,LOW);
  SysBits=EEPROM.read(EE_SysBits);
  RssMax=EEPROM.read(EE_RssMax);
  if (RssMax==255) {RssMax=0;}  //not real yet? Reset reference value
  RssMin=EEPROM.read(EE_RssMin); //255 is OK as a 'not real yet' reference value
    
  Serial.begin(57600);  vw_setup(4800);  vw_rx_start();
  
  ShowResponse(0,1); 
  ShowResponse(2,0); Serial.print(RssMax);
  ShowResponse(3,0); Serial.println(RssMin);
  Serial.println("* Setup complete");
} 

void loop() { GetRssMin();
  if (vw_have_message()) { CheckRX(); }
  else {CheckPCbuf(); }
}

//*********** End of Main *******************
//*******************************************

// V V V V V V  Functions V V V V V V V V V V 

void CheckRX() {   uint8_t readBuffer[VW_MAX_MESSAGE_LEN];  uint8_t bufferLength = VW_MAX_MESSAGE_LEN;
    RssNow=GetRssPct(); 
    vw_get_message(readBuffer, &bufferLength);
    char checkSumByte;  char transmissionString[40];
    *transmissionString = 0; 
    for (int i = 0; i < bufferLength; i++) {
      if (i == (bufferLength - 1)) { checkSumByte = readBuffer[i]; transmissionString[i] = 0; }
      else { transmissionString[i] = readBuffer[i]; }  }
      
    digitalWrite(pin_LED_POWER, HIGH);
    if (checkSumByte == makeCheckSumByte(transmissionString, strlen(transmissionString))) {
       PrntHdr(); Serial.println(transmissionString);   }
    else { transmissionString[bufferLength-1]=checkSumByte; 
             transmissionString[bufferLength] = 0;
      Serial.print("* "); PrntHdr();  Serial.println(transmissionString); }
    digitalWrite(pin_LED_POWER,LOW);  
}// EO_CheckRX
  
void CheckPCbuf() {  if (Serial.available() > 0)  {  char ch; int pk; byte cptr; char PCbuf[50];
    cptr=0; ch = Serial.read();
    while ((ch != '\n' && ch != '\r'))  {
      PCbuf[cptr] = ch; cptr++; 
      pk = Serial.peek(); while (pk<0) { pk = Serial.peek(); } 
      ch = Serial.read(); }
    PCbuf[cptr] = 0;
    ch = Serial.peek(); if (ch == '\n' || ch == '\r') {ch = Serial.read();}
    Serial.println(PCbuf); 
    if (String(PCbuf)=="?") { ShowHelp(); }
    else if (String(PCbuf) == "ver") { ShowResponse(0,1); } 
    else if (String(PCbuf) == "rssmm") { ResetRSS(); ShowResponse(1,1); } 
    PCbuf[0]=0;}
} // EO_CheckPCbuf 

byte GetRssPct () { int RssVal; RssVal=analogRead(pin_RSS);  //toss the first reading
  RssVal=(analogRead(pin_RSS)+analogRead(pin_RSS)+analogRead(pin_RSS))/12; //average 3 - make byte-size
  if (RssVal>RssMax) {RssMax=RssVal;EEPROM.write(EE_RssMax,RssMax);}
  RssVal=((RssVal-RssMin) *100 ) / (RssMax-RssMin) ; 
  if (RssVal>100) {RssVal=100;}  if (RssVal<0) {RssVal=0;}
  return byte(RssVal); }

void ResetRSS() { RssMin=255;  EEPROM.write(EE_RssMin,RssMin);
                  RssMax=0;   EEPROM.write(EE_RssMax,RssMax); } 

void PrntHdr() {Serial.print("RX|");Serial.print(RssNow);Serial.print("%|"); } 

void GetRssMin() {int RssVal; RssVal=analogRead(pin_RSS); 
  for (int x=10;x>0;x--) {RssVal= (RssVal + analogRead(pin_RSS))/2; }
  RssVal=RssVal/4; //make byte-size
  if (RssVal<RssMin) {RssMin=RssVal; EEPROM.write(EE_RssMin,RssMin);}
} 

byte makeCheckSumByte(char* transmission, int transmissionLength) {
  byte checkSumByte = 0;
  for (int i = 0; i < transmissionLength; i++) {
    checkSumByte = checkSumByte ^ transmission[i];
  }
  return checkSumByte;
}

void ShowHelp() {char sHelp[80]; for (byte x=0; x<HLPlim; x++) {*sHelp=0;
  strcat_P(sHelp, (char*)pgm_read_word(&(table_HELP[x]))); Serial.println(sHelp);} 
} //________ END OF ShowHelp _____________ 


//*******************
void ShowResponse(byte RespNum, byte crlf) {char sResp[80]; *sResp=0;
  strcat_P(sResp, (char*)pgm_read_word(&(table_RESP[RespNum])));
  if (crlf==1) {Serial.println(sResp);} else {Serial.print(sResp);}
} //________ END OF ShowResponse _____________ 





