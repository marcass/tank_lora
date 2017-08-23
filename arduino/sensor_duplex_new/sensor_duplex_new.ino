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


int counter = 0;
//*****************Change the following 2 variables ************
/*Assign node numbers
 * 1. Top tank
 * 2. Noels break
 * 3. Sal's bush
 * Main?
 * Bay?
 */
const int NODE_ID = 5;
#define SS 1                  //NSS pin def for lora lib, use "1" for older modules and "8" for new modules (they have clearer text on ATMEL chip)
//**************************************************************
const int V_CAL = 442;  //calibration analogRead(V_POWER) @4.2v for individual prcessor

#define V_PIN  0             //measure voltage off this pin
#define WAKE_PIN 2           //wake pin on D2 (interrupt 0)
#define POWER  3             //Power up n-channel mosfet to read distance
#define RESET  4             //RESET pin for lora radio
#define V_POWER 5            //pull down p-channel mosfet to measure voltage
#define DIO  7               //DIO 0  for lora lib
#define DONE  9              //Done pulse goes here
#define TRIGPIN  11          // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHOPIN     12       // Arduino pin tied to echo pin on the ultrasonic sensor.

//allowed to forward for sals - more verstile than using syncword
const byte ALLOWED = 0xFF;
bool wake_resp;
int dist;
byte DONE_T = 1;
bool intitialisePins;
float voltage;
unsigned long send_timer;
unsigned long wake_delay;
const unsigned long SEND_THRESH = 360000; //6min

//LoRa radio setup https://github.com/sandeepmistry/arduino-LoRa/blob/master/API.md
//Lower number if closer receiver (saves power)
//LoRa.setTxPower(txPower); //Supported values are between 2 and 17 for PA_OUTPUT_PA_BOOST_PIN, 0 and 14 for PA_OUTPUT_RFO_PIN.

void setup() {
  //.setup analog ref for battery testing
  analogReference(INTERNAL); //measures at 1.1V ref to give a value for flaoting voltage form batt
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
  //set up for external watchdog patting
  attachInterrupt(digitalPinToInterrupt(WAKE_PIN), wake, RISING);
  wake_resp = false;
}

//battery testing function
//A3 connected to voltage divider form battery, this is turned on by D0
// see http://fettricks.blogspot.co.nz/2014/01/reducing-voltage-divider-load-to-extend.html
//specified voltage divider (3.74kOhnm high side and 10k to drain) gives a 4.2V down converted to 1.14V)

void batteryMeasure() {
  digitalWrite(V_POWER, LOW);//close mosfet to measure
  delayMicroseconds(20); //wait for cap to discharge before reading
  //Serial.print("Value of measure pin is: ");
  int val = analogRead(V_PIN); //measure analog val for conversion
  //Serial.println(val);
  digitalWrite(V_POWER, HIGH);//open mosfet to conserve power
  //convert. Returns actual voltage, ie 3.768 = 3.768V
  voltage = (((float)val / V_CAL) * 1.1) / (1.1 / 4.2);
  #ifdef debug
    Serial.print("Analog read = ");
    Serial.println(val);
    Serial.print(", Voltage = ");
    Serial.println(voltage);
  #endif
}

void distMeasure(){
  digitalWrite(POWER, HIGH);
  delay(10); //measured as needing to be above 280ms for saturation of boost converter
  digitalWrite(TRIGPIN, LOW); // Set the trigger pin to low for 2uS
  delayMicroseconds(2);
  digitalWrite(TRIGPIN, HIGH); // Send a 10uS high to trigger ranging
  delayMicroseconds(10);
  digitalWrite(TRIGPIN, LOW); // Send pin low again
  unsigned long pulse = pulseIn(ECHOPIN, HIGH,26000); // Read in times pulse
  dist= pulse/58;
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

void wake (){
  wake_resp = true;
  wake_delay = millis();
}  // end of wake

void onReceive(int packetSize) {
  if (packetSize == 0) return;          // if there's no packet, return

  // read packet header bytes:
  byte sender = LoRa.read();            // sender address

  // if the recipient isn't this device or broadcast,
  if (sender != ALLOWED) {
    #ifdef debug
      Serial.println("This message is not for me.");
    #endif
    return;                             // skip rest of function
  }

  //otherwise build the string
  String incoming = "";

  while (LoRa.available()) {
    incoming += (char)LoRa.read();
  }

  //forward the packet
  LoRa.beginPacket();
  LoRa.print(incoming);
  LoRa.endPacket();

  #ifdef debug
    // if message is for this device, or broadcast, print details:
    Serial.println("Received from: 0x" + String(sender, HEX));
    Serial.println("Message: " + incoming);
    Serial.println("RSSI: " + String(LoRa.packetRssi()));
    Serial.println("Snr: " + String(LoRa.packetSnr()));
    Serial.println();
  #endif
}

void send_local_data(){
  batteryMeasure();
  distMeasure();
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
}
void loop() {
//send local data now and then
  if (millis() - send_timer > SEND_THRESH) {
    send_local_data();
    send_timer = millis();
  }
  if (wake_resp){
    //TPL5010 sends a 20ms high pulse. It expexts a response to 'DONE' pin sometime after 20ms
    if (millis() - wake_delay > 30){
      //Send successful wake pulse to external watchdog
      digitalWrite(DONE, HIGH);
      delayMicroseconds(DONE_T);
      digitalWrite(DONE, LOW);
      wake_resp = false;
    }
  }

  // parse for a packet, and call onReceive with the result:
  onReceive(LoRa.parsePacket());
}



