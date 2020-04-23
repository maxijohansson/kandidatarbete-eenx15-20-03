#include "RunningMedian.h"

static int pinA = 2;
static int pinB = 3;
volatile byte aFlag = 0;
volatile byte bFlag = 0;
volatile byte reading = 0;

volatile int newTime = 0;
volatile int oldTime = 0;
volatile uint32_t elapsedTime = 0;
volatile int medElapsedTime = 0;
volatile byte counter = 0;
volatile float medSpeed = 0;
static int distancePerRotation = 0.1115 * 1000; // The distance in millimeters the car travels under one rotation of the encoder wheel
static int distancePerClick = distancePerRotation/20;

boolean flag = true;
volatile int calc_speed = 0;

RunningMedian samples = RunningMedian(10);

void setup() {
  
  pinMode(pinA, INPUT_PULLUP);
  pinMode(pinB, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(pinA),pinATrig,RISING);
  attachInterrupt(digitalPinToInterrupt(pinB),pinBTrig,RISING);
  Serial.begin(115200);
  Serial.println("Starting");
  
}

void pinATrig() {
  cli();
  if (reading == B00001100 && aFlag) {
    aFlag = 0;
    bFlag = 0;
    //Serial.println("pin A");
  }
  else if (reading == B00000100) bFlag = 1;

  sei();
}

void pinBTrig() {
  cli();
  reading = PIND & 0xC;
  if (reading == B00001100 && bFlag) {
    aFlag = 0;
    bFlag = 0;
    counter++;
  }
  else if (reading == B00001000) aFlag = 1;

  sei();
}

void loop() {
  if (millis() % 200 == 0 && flag == true) {
    newTime = millis();
    elapsedTime = newTime - oldTime;
    calc_speed = (1000 * counter * distancePerClick) / (elapsedTime);
    oldTime = millis();
    
    Serial.print(calc_speed);
    Serial.print("        ");
    Serial.print(elapsedTime);
    Serial.print("        ");
    Serial.println(counter);
    counter = 0;
    delay(1);
    //Serial.print("speed: ");
    //Serial.println(medSpeed);
    
  }
  
}
