/*******Interrupt-based Rotary Encoder Sketch*******
  by Simon Merrett, based on insight from Oleg Mazurov, Nick Gammon, rt, Steve Spence
*/
#include <MemoryFree.h>

volatile uint32_t newTime = 0;
volatile uint32_t oldTime = 0;
volatile uint32_t elapsedTime = 0;
volatile float calc_speed = 0;
static float distancePerRotation = 0.1115; // The distance in meters the car travels under one rotation of the encoder wheel
static float distancePerClick = distancePerRotation/20.0;

static int pinA = 2; // Our first hardware interrupt pin is digital pin 2
static int pinB = 3; // Our second hardware interrupt pin is digital pin 3
volatile byte aFlag = 0; // let's us know when we're expecting a rising edge on pinA to signal that the encoder has arrived at a detent
volatile byte bFlag = 0; // let's us know when we're expecting a rising edge on pinB to signal that the encoder has arrived at a detent (opposite direction to when aFlag is set)
volatile byte encoderPos = 0; //this variable stores our current value of encoder position. Change to int or uin16_t instead of byte if you want to record a larger range than 0-255
volatile byte oldEncPos = 0; //stores the last encoder position value so we can compare to the current reading and see if it has changed (so we know when to print to the serial monitor)
volatile byte reading = 0; //somewhere to store the direct values we read from our interrupt pins before checking to see if we have moved a whole detent
volatile uint16_t counter = 0;
volatile int adding = 0;

void setup() {
  pinMode(pinA, INPUT_PULLUP); // set pinA as an input, pulled HIGH to the logic voltage (5V or 3.3V for most cases)
  pinMode(pinB, INPUT_PULLUP); // set pinB as an input, pulled HIGH to the logic voltage (5V or 3.3V for most cases)
  attachInterrupt(0, PinA, RISING); // set an interrupt on PinA, looking for a rising edge signal and executing the "PinA" Interrupt Service Routine (below)
  attachInterrupt(1, PinB, RISING); // set an interrupt on PinB, looking for a rising edge signal and executing the "PinB" Interrupt Service Routine (below)
  Serial.begin(115200); // start the serial monitor link
  Serial.println("Starting");
  Serial.println(distancePerClick, 4);
}

void PinA() {
  cli(); //stop interrupts happening before we read pin values
  reading = PIND & 0xC; // read all eight pin values then strip away all but pinA and pinB's values
  if (reading == B00001100 && aFlag) { //check that we have both pins at detent (HIGH) and that we are expecting detent on this pin's rising edge
    counter ++;
    //encoderPos --; //decrement the encoder's position count
    bFlag = 0; //reset flags for the next turn
    aFlag = 0; //reset flags for the next turn
  }
  else if (reading == B00000100) bFlag = 1; //signal that we're expecting pinB to signal the transition to detent from free rotation
  sei(); //restart interrupts
}

void PinB() {
  cli(); //stop interrupts happening before we read pin values
  reading = PIND & 0xC; //read all eight pin values then strip away all but pinA and pinB's values
  if (reading == B00001100 && bFlag) { //check that we have both pins at detent (HIGH) and that we are expecting detent on this pin's rising edge
    counter --;
    //encoderPos ++; //increment the encoder's position count
    bFlag = 0; //reset flags for the next turn
    aFlag = 0; //reset flags for the next turn
  }
  else if (reading == B00001000) aFlag = 1; //signal that we're expecting pinA to signal the transition to detent from free rotation
  sei(); //restart interrupts
}

void loop() {
  //  if(oldEncPos != encoderPos) {
  //    Serial.println(encoderPos);
  //    oldEncPos = encoderPos;
  if (millis() % 200 == 0) {
    newTime = micros();
    elapsedTime = newTime - oldTime;
    adding ++;
    calc_speed = (1000000.0 * float(counter) * distancePerClick) / (float(elapsedTime)); // Hastighet i m/s
    oldTime = micros();
    

    Serial.print(calc_speed, 4);
    Serial.print("        ");
    Serial.print(elapsedTime);
    Serial.print("        ");
    Serial.print(counter);
    Serial.print("        ");
    Serial.println(freeMemory());
  
    counter = 0;
    delay(1);
    //Serial.print("speed: ");
    //Serial.println(medSpeed);

  }
}
