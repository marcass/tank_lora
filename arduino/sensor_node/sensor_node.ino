/* TODO
 *  chjeck brownout and watrchdog is disables
 *  check that we can wake with ahigh level trigger (think it needs to be low according to datasheet
 *  set internal voltage level in getbandgap https://www.gammon.com.au/forum/?id=11497
 */  


#include <SPI.h>
#include <LoRa.h>
//Sonar stuff
//sleep stuff http://www.engblaze.com/hush-little-microprocessor-avr-and-arduino-sleep-mode-basics/
#include <avr/interrupt.h>
#include <avr/power.h>
#include <avr/sleep.h>
#include <avr/io.h>
#include <NewPing.h>

//debug
#define debug

int counter = 0;
/*Assign node numbers
 * 1. Top tank
 * 2. Noels break
 * 2. Sal's bush
 */
const int NODE_ID = 1;

#define SS 1                  //NSS pin def for lora lib
#define V_PIN  0             //measure voltage off this pin
#define WAKE_PIN 2            //wake pin on D2 (interrupt 0)
#define POWER  3             //Power up n-channel mosfet to read distance
#define RESET  4             //RESET pin for lora radio
#define V_POWER 5            //pull down p-channel mosfet to measure voltage
#define DIO  7               //DIO 0  for lora lib
#define DONE  9              //Done pulse goes here
#define TRIGGER_PIN  11       // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     12       // Arduino pin tied to echo pin on the ultrasonic sensor.


byte DONE_T = 1;
bool intitialisePins;
float voltage;

//ultrasonic setup
#define MAX_DISTANCE 300 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.
int dist;
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.


//LoRa radio setup https://github.com/sandeepmistry/arduino-LoRa/blob/master/API.md
//Lower number if closer receiver (saves power)
//LoRa.setTxPower(txPower); //Supported values are between 2 and 17 for PA_OUTPUT_PA_BOOST_PIN, 0 and 14 for PA_OUTPUT_RFO_PIN.

void setup() {
  
  //disable sleep bit:
  sleep_disable();
  pinMode(DONE, OUTPUT);
  digitalWrite(DONE, LOW);
  pinMode(POWER, OUTPUT);
  digitalWrite(POWER, LOW);
  pinMode(V_POWER, OUTPUT);
  digitalWrite(V_POWER, HIGH);
 
  #ifdef debug
    Serial.begin(9600);
    while (!Serial); //uncomment to require serial connection to work
    Serial.println("LoRa Sender");
  #endif
  
  LoRa.setPins(SS, RESET, DIO); 
  if (!LoRa.begin(433E6)) { // initialise at 433MHz
    #ifdef debug
      Serial.println("Starting LoRa failed!");
    #endif
    while (1);
  }
  //.setup analog ref for battery testing
  analogReference(INTERNAL); //measures at 1.1V ref to give a value for flaoting voltage form batt

}

//battery testing function
//A3 connected to voltage divider form battery, this is turned on by D0
// see http://fettricks.blogspot.co.nz/2014/01/reducing-voltage-divider-load-to-extend.html
//specified voltage divider (3.74kOhnm high side and 10k to drain) gives a 4.2V down converted to 1.14V)

void batteryMeasure() {
  digitalWrite(POWER, LOW);//close mosfet to measure
  delayMicroseconds(20); //wait for cap to discharge before reading
  //Serial.print("Value of measure pin is: ");
  int val = analogRead(V_measurePin); //measure analog val for conversion
  //Serial.println(val);
  digitalWrite(POWER, HIGH);//open mosfet to conserve power
  //convert. Returns actual voltage, ie 3.768 = 3.768V
  voltage = (((float)val / 442) * 1.1) / (1.1 / 4.2);
}

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
  
    // send packet
    LoRa.beginPacket();
    LoRa.print("NodeID ");
    LoRa.print(NODE_ID);
    LoRa.print("count ");
    LoRa.print(counter);
    LoRa.endPacket();
  
    counter++;
  
    delay(5000);
  #endif
  
  batteryMeasure();
  digitalWrite(V_POWER, HIGH);
  //send distance to water
  //power up ultrasonic sensor
  digitalWrite(POWER, HIGH);
  delay(5); //wait for board to warm up
  Serial.print(sonar.ping_cm());
  //dist = sonar.ping_cm();
  //TURN u/s module off
  digitalWrite(POWER, LOW);
  //send packet
  LoRa.beginPacket();
  LoRa.print("PY:");//tag for serial listner
  LoRa.print(NODE_ID);
  LoRa.print(";");
  LoRa.print(dist);
  LoRa.print(";");
  LoRa.print(voltage);
  LoRa.print(";");
  LoRa.endPacket();
  sleepNow();
  //Send successful wake pulse to external watchdog
  digitalWrite(DONE, HIGH);
  delayMicroseconds(DONE_T);
  digitalWrite(DONE, LOW);
  //start loop again
}



