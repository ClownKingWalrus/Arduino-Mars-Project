#include "SevSeg.h"
const int led = 22;
const int sensorPin = A0;
int sensor;
const int threshHold = 400;
int battery = 100;
//inialize seven seg object
//.setNumber(numberyouWant, decimalPlace_rightToLeft)
SevSeg sevSeg;

//how to test clock
// sevSeg.setNumber(8751, 3);
// sevSeg.refreshDisplay(); <- must run constantly


void setup() {
  pinMode(led, OUTPUT);
  Serial.begin(9600);
  //initlize the clock pins
  //initlizing Clock Digits 4 digits in total
  byte numDigits = 4;
  byte digitPins[] = {10, 11, 12, 13}; // the pins the each digit is hooked up to in order since power runs through this pins place resistors
  byte segementPins[] = {9, 2, 3, 5, 6, 8, 7, 4}; //each segement in pins
  bool resistorOnSegements = true;
  byte hardwareConfig = COMMON_CATHODE;
  //start clock and make the brightness visable
  sevSeg.begin(hardwareConfig, numDigits, digitPins, segementPins, resistorOnSegements);
  sevSeg.setBrightness(90);
}

void wait(int timeMs) {
  unsigned long startTime = millis();
  while (millis() - startTime <= timeMs) // end time - start time = time taken. time taken < timeMs = length of time allowed for loop
  {
    sevSeg.refreshDisplay();
  }
}

void loop() {
  sensor = analogRead(sensorPin);
  Serial.println(battery);
  if (sensor > threshHold) {
    //tester for serial
    // if (battery > 10) {
    //   Serial.println("ENDING SERIAL");
    //   Serial.end();
    //   return;
    // }
    digitalWrite (led, LOW);
    battery++;
    sevSeg.setNumber(battery);
    wait(500);
  } 
  //check if we still have battery
  else if (battery > 0 && sensor < threshHold) {
    battery--;
    digitalWrite(led, HIGH);
    sevSeg.setNumber(battery);
    wait(1000);
  } 
  //no battery left led goes off
  else {
    digitalWrite(led,LOW);
    sevSeg.setNumber(battery);
    wait(100);
  }
}
