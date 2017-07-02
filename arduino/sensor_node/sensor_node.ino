/* TODO
 *  chjeck brownout and watrchdog is disables
 *  check that we can wake with ahigh level trigger (think it needs to be low according to datasheet
 *  check pin register stuff in setup
 */  

#include <SPI.h>
#include <LoRa.h>
//Sonar stuff
#include <NewPing.h>
//sleep stuff http://www.engblaze.com/hush-little-microprocessor-avr-and-arduino-sleep-mode-basics/
#include <avr/interrupt.h>
#include <avr/power.h>
#include <avr/sleep.h>
#include <avr/io.h>

//debug
#define debug
//#define sensor

int counter = 0;
/*Assign node numbers
 * 1. Top tank
 * 2. Noels break
 * 2. Sal's bush
 */
int sensor_node = 1;

//ultrasonic setup
#define TRIGGER_PIN  4  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     5  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 400 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.
int distance;
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

void setup() {
  #ifdef sensor
    //power management at pins - check what newping needs for trig and echo
    DDRD &= B00000011;       // set Arduino pins 2 to 7 as inputs, leaves 0 & 1 (RX & TX) as is
    DDRB = B00000000;        // set pins 8 to 13 as inputs
    PORTD |= B11111000;      // enable pullups on pins 3 to 7, leave pins 0,1 and 2 (high level interrupt) alone - modified by mw
    PORTB |= B11111111;      // enable pullups on pins 8 to 13
    pinMode(13,OUTPUT);      // set pin 13 as an output so we can use LED to monitor
  #endif
  
  Serial.begin(9600);
  while (!Serial);

  Serial.println("LoRa Sender");

  if (!LoRa.begin(433E6)) { // initialise at 433MHz
    Serial.println("Starting LoRa failed!");
    while (1);
  }
}

void loop() {
  #ifdef debug
    Serial.print("Sending packet: ");
    Serial.println(counter);
  
    // send packet
    LoRa.beginPacket();
    LoRa.print("NodeID ");
    LoRa.print(sensor_node);
    LoRa.print("count ");
    LoRa.print(counter);
    LoRa.endPacket();
  
    counter++;
  
    delay(5000);
  #endif

  #ifdef sensor
    distance = sonar.ping_cm();
    LoRa.beginPacket();
    //configure MyController packet: set,req described here: https://www.mysensors.org/download/serial_api_20
    LoRa.print("NodeID");
    LoRa.print(";1;1;1;13;");
    LoRa.print(distance);
    LoRa.endPacket();
    //go to sleep when done
    sleepNow();
    //delay(10000); //10s between measurements for testing
  #endif
}


void sleepNow(){
  // Set pin 2 as interrupt and attach handler:
  attachInterrupt(0, pinInterrupt, HIGH); //TPL5010 sends high pulse to pin 2
  delay(100);
  // Choose our preferred sleep mode:
  set_sleep_mode(SLEEP_MODE_PWR_DOWN};

  // Set sleep enable (SE) bit:
  sleep_enable();

  // Put the device to sleep:
  sleep_mode();

  // Upon waking up, sketch continues from this point.
  sleep_disable();
}

//Handler for wake inturrupt detaches interrupt
void pinInterrupt(void){
  detachInterrupt(0);
}
