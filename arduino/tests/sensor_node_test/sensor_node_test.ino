#include <NewPing.h>

#include <SPI.h>
#include <LoRa.h>
//Sonar stuff
//sleep stuff http://www.engblaze.com/hush-little-microprocessor-avr-and-arduino-sleep-mode-basics/
#include <avr/interrupt.h>
#include <avr/power.h>
#include <avr/sleep.h>
#include <avr/io.h>

//debug
//#define debug
//#define forwarded  //uncomment if node needs to be forwarded
//#define rapid
#define sleeping

#ifdef forwarded
  byte destination = 0xFF;
#endif

int counter = 0;

//*****************Change the following 2 variables ************
/*Assign node numbers
 * 1. Top tank
 * 2. Noels break
 * 3. Sal's bush
 * Main?
 * Bay?
 */
const int NODE_ID = 1;
const int V_CAL = 442;  //calibration analogRead(V_POWER) for individual prcessor

#define SS 1                  //NSS pin def for lora lib, use "1" for older modules and "8" for new modules (they have clearer text on ATMEL chip)
#define V_PIN  3             //measure voltage off this pin
#define WAKE_PIN 2           //wake pin on D2 (interrupt 0)
#define POWER  3             //Power up n-channel mosfet to read distance
#define RESET  4             //RESET pin for lora radio
#define V_POWER 5            //pull down p-channel mosfet to measure voltage
#define DIO  7               //DIO 0  for lora lib
#define DONE  9              //Done pulse goes here
#define TRIGPIN  11          // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHOPIN     12       // Arduino pin tied to echo pin on the ultrasonic sensor.

NewPing sonar(TRIGPIN, ECHOPIN, 250);

int val;
int dist;
byte DONE_T = 1;
bool intitialisePins;
float voltage;

//LoRa radio setup https://github.com/sandeepmistry/arduino-LoRa/blob/master/API.md
//Lower number if closer receiver (saves power)
//LoRa.setTxPower(txPower); //Supported values are between 2 and 17 for PA_OUTPUT_PA_BOOST_PIN, 0 and 14 for PA_OUTPUT_RFO_PIN.

void setup() {
  //.setup analog ref for battery testing
  analogReference(INTERNAL); //measures at 1.1V ref to give a value for flaoting voltage form batt
  delay(50); //allow voltage to settle
  //disable sleep bit:
  sleep_disable();
  pinMode(DONE, OUTPUT);
  digitalWrite(DONE, LOW);
  pinMode(POWER, OUTPUT);
  digitalWrite(POWER, LOW);
  pinMode(V_POWER, OUTPUT);
  digitalWrite(V_POWER, HIGH);
  //ultrasonic pins
  pinMode(ECHOPIN, INPUT_PULLUP);
  pinMode(TRIGPIN, OUTPUT);
  digitalWrite(TRIGPIN, LOW);
 
  #ifdef debug
    Serial.begin(9600);
    //while (!Serial); //uncomment to require serial connection to work
    Serial.println("LoRa Sender");
  #endif
  
  LoRa.setPins(SS, RESET, DIO); 
  if (!LoRa.begin(433E6)) { // initialise at 433MHz
    #ifdef debug
      Serial.println("Starting LoRa failed!");
    #endif
    while (1);
  }
}

//battery testing function
//A3 connected to voltage divider form battery, this is turned on by D0
// see http://fettricks.blogspot.co.nz/2014/01/reducing-voltage-divider-load-to-extend.html
//specified voltage divider (3.74kOhnm high side and 10k to drain) gives a 4.2V down converted to 1.14V)

void batteryMeasure() {
  digitalWrite(V_POWER, LOW);//close mosfet to measure
  delayMicroseconds(20); //wait for cap to discharge before reading
  //Serial.print("Value of measure pin is: ");
  val = analogRead(V_PIN); //measure analog val for conversion
  //Serial.println(val);
  digitalWrite(V_POWER, HIGH);//open mosfet to conserve power
  //convert. Returns actual voltage, ie 3.768 = 3.768V
  voltage = (((float)val / V_CAL) * 1.1) / (1.1 / 4.2);
  #ifdef debug
    Serial.print("Analog read = ");
    Serial.println(val);
    Serial.print("Voltage = ");
    Serial.println(voltage);
  #endif
}

void distMeasure(){
  digitalWrite(POWER, HIGH);
  delay(10); //measured as needing to be above 280ms for saturation of boost converter
  digitalWrite(TRIGPIN, LOW); // Set the trigger pin to low for 2uS for clean pulse
  delayMicroseconds(2);
  digitalWrite(TRIGPIN, HIGH); // Send a 10uS high to trigger ranging
  delayMicroseconds(10);
  digitalWrite(TRIGPIN, LOW); // Send pin low again
  unsigned long pulse = pulseIn(ECHOPIN, HIGH,26000); // Read in times pulse
  dist = pulse/58;
  #ifdef debug
    Serial.print("pulse = ");
    Serial.print(pulse);
    Serial.print(", dist = ");
    Serial.print(dist);
    Serial.println("cm"); 
  #endif
  //power down mosfet
  digitalWrite(POWER, LOW);                   
}

//void distMeasure(){
//  unsigned long pulse_start;
//  unsigned long pulse;
//  unsigned long pulse_inc;
//  digitalWrite(POWER, HIGH);
//  delay(350); //measured as needing to be above 280ms for saturation of boost converter
//  digitalWrite(TRIGPIN, LOW); // Set the trigger pin to low for 2uS for clean pulse
//  delayMicroseconds(2);
//  digitalWrite(TRIGPIN, HIGH); // Send a 10uS high to trigger ranging
//  delayMicroseconds(10);
//  digitalWrite(TRIGPIN, LOW); // Send pin low again
//  //no longer high so start counter
//  pulse_start = micros();
//  while(digitalRead(ECHOPIN) == LOW){
//    //do nothing
//  }
//  //no longer high so start counter
//  //pulse_start = micros();
//  while(digitalRead(ECHOPIN) == HIGH){
//    //increment counter
//    pulse_inc = micros();
//  }
//  //echo pin no longer high so reading finished
//  pulse = pulse_inc - pulse_start;
//  dist = pulse/58;
//  #ifdef debug
//    Serial.print("pulse = ");
//    Serial.print(pulse);
//    Serial.print(", dist = ");
//    Serial.print(dist);
//    Serial.println("   cm"); 
//  #endif
//  //power down mosfet
//  digitalWrite(POWER, LOW);                   
//}
void wake (){
  // cancel sleep as a precaution
  sleep_disable();
  // precautionary while we do other stuff
  detachInterrupt(digitalPinToInterrupt(WAKE_PIN));
}  // end of wake

void sleepNow(){ //see https://www.gammon.com.au/forum/?id=11497

  //sleep lora radio
  LoRa.sleep();
  
  // Choose our preferred sleep mode:
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  
  //power_all_disable();//disables power to all modules careful here as not sure how to wake up
  // Set sleep enable (SE) bit:
  sleep_enable();
  
  // Do not interrupt before we go to sleep, or the
  // ISR will detach interrupts and we won't wake.
  noInterrupts();           // timed sequence follows
  
  // will be called when pin D2 goes high  
  attachInterrupt(digitalPinToInterrupt(WAKE_PIN), wake, RISING);
  
  // We are guaranteed that the sleep_cpu call will be done
  // as the processor executes the next instruction after
  // interrupts are turned on.
  interrupts();  // one cycle
  sleep_cpu();   // one cycle
}

void loop() {
  #ifdef debug
    Serial.print("Sending packet: ");
    Serial.println(counter);
    counter++;
  
    //delay(5000);
  #endif
  
  batteryMeasure();
  distMeasure();
  //send packet
  LoRa.beginPacket();
  #ifdef forwarded
    LoRa.write(destination);
  #endif
  LoRa.print("PY;");//tag for serial listner
  LoRa.print(NODE_ID);
  LoRa.print(";");
  LoRa.print(dist);
  LoRa.print(";");
  LoRa.print(voltage);
  LoRa.print(";");
  LoRa.endPacket();
  #ifdef sleeping
    //Send successful wake pulse to external watchdog
    //pause for wake pulse calming (needs 20ms and measuring may not take that long)
    delay(20);
    digitalWrite(DONE, HIGH);
    delayMicroseconds(DONE_T);
    digitalWrite(DONE, LOW);
    sleepNow();
  #endif
  #ifdef rapid
    //LoRa.sleep();
    delay(3000);
  #endif
  //start loop again
}



