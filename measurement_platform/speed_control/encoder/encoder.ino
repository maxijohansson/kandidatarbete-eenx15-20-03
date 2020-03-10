#include "RunningMedian.h"

static int pinA = 2;
static int pinB = 3;
volatile byte aFlag = 0;
volatile byte bFlag = 0;
volatile byte reading = 0;

volatile int newTime = 0;
volatile int oldTime = 0;
volatile int elapsedTime = 0;
volatile int medElapsedTime = 0;
volatile int counter = 0;
volatile float medSpeed = 0;
static float distancePerRotation = 0.1115; // The distance in meters the car travels under one rotation of the encoder wheel
static float distancePerClick = distancePerRotation/20;


RunningMedian samples = RunningMedian(10);

void setup() {
  pinMode(pinA, INPUT_PULLUP);
  pinMode(pinB, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(pinA),pinATrig,RISING);
  attachInterrupt(digitalPinToInterrupt(pinB),pinBTrig,RISING);
  Serial.begin(9600);
  Serial.println("Starting");
  
}

void pinATrig() {
  cli();
  reading = PIND & 0xC;
  if (reading == B00001100 && aFlag) {
    aFlag = 0;
    bFlag = 0;
    Serial.println("pin A");
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
    newTime = millis();
    elapsedTime = newTime - oldTime;
    samples.add(elapsedTime);
    medSpeed = distancePerClick / (0.001*samples.getMedian());
    counter++;
    oldTime = millis();
    // Serial.print("pin B: ");
    // Serial.println(elapsedTime);
  }
  else if (reading == B00001000) aFlag = 1;

  sei();
}

void loop() {
  if (millis() % 200 == 0) {
    Serial.print("speed: ");
    Serial.println(medSpeed);
    delay(10);
  }
}
