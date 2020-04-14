#include "RunningMedian.h"
#include "ESC.h"
#define SPEED_MIN (1000)                                  // Set the Minimum Speed in microseconds
#define SPEED_MAX (2000)  

ESC myESC (9, SPEED_MIN, SPEED_MAX, 500);   
int oESC;           

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
int pwm;
float Kp, Ki, e, e_old, target, u;

float I_old = 0;
float I = 0;
float P = 0;

RunningMedian samples = RunningMedian(10);

void setup() {
  cli();
  target = 5/3.6; //Börvärde m/s
  Kp = 1; // Proportionalitetskonstant
  Ki = 0; //Intergralkonstant
  e = 0;
  pinMode(pinA, INPUT_PULLUP);
  pinMode(pinB, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(pinA),pinATrig,RISING);
  attachInterrupt(digitalPinToInterrupt(pinB),pinBTrig,RISING);
  Serial.begin(9600);
  Serial.println("Starting");
  myESC.arm();  
  delay(100); 
  //pinMode(7, INPUT);
  counter = 0;
  sei();
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
    //Serial.print("speed: ");
    Serial.println(medSpeed);
    delay(10);
  }
  controller(medSpeed);
  /*
  if(digitalRead(7) == HIGH){
    Serial.println("Stopping");
    exit(0);
  }*/
  delay(10);
}
  
void controller(float v){
  e_old = e;
  e = target - v;
  P = Kp * e;
  I_old = I;
  I = I_old + Ki * 0.02 * e;

  u = P + I;
  pwm = 1500 - u; 
  myESC.speed(1450);
  //Serial.print("PWM signal: ");
  //Serial.println(pwm);
  //Serial.println(I);
  //Serial.println(v);  
  Serial.print(e);
  //Serial.println(target);
  Serial.print("  ");
  Serial.print(v);
  Serial.print("  ");
  Serial.println(u);
  delay(10);
}
