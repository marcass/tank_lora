#include <SPI.h>
#include <LoRa.h>
#include <avr/interrupt.h>
#include <avr/power.h>
#include <avr/sleep.h>
#include <avr/io.h>

//debug
//#define debug

//allowed to forward for sals - more verstile than using syncword
const byte ALLOWED = 0xFF;
bool wake_resp;
const int DONE_T = 1;
unsigned long send_timer;
const unsigned long SEND_THRESH = 360000; //6min
//set tx power Supported values are between 2 and 17
const int TX_POWER = 8;

#define SS 8                //NSS pin def for lora lib (set to 8 for new modules
#define V_PIN  3             //measure voltage off this pin
#define WAKE_PIN 2           //wake pin on D2 (interrupt 0)
#define RESET  4             //RESET pin for lora radio
#define V_POWER 5            //pull down p-channel mosfet to measure voltage
#define DIO  7               //DIO 0  for lora lib
#define DONE  9              //Done pulse goes here

const int NODE_ID = 6; //SET THIS FOR NODE 
float voltage;
byte tag = 0xAA;
byte MAINTOP = 0xCC;
byte SALS = 0xFF;

//LoRa radio setup https://github.com/sandeepmistry/arduino-LoRa/blob/master/API.md
//Lower number if closer receiver (saves power)
//LoRa.setTxPower(txPower); //Supported values are between 2 and 17 for PA_OUTPUT_PA_BOOST_PIN, 0 and 14 for PA_OUTPUT_RFO_PIN.

void setup() {
  send_timer = millis();
  pinMode(DONE, OUTPUT);
  digitalWrite(DONE, LOW);
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
  LoRa.setTxPower(TX_POWER);
  //.setup analog ref for battery testing
  analogReference(INTERNAL); //measures at 1.1V ref to give a value for flaoting voltage form batt
  //set up for external watchdog
  attachInterrupt(digitalPinToInterrupt(WAKE_PIN), wake, RISING);
  wake_resp = false;
}

//battery testing function
//A3 connected to voltage divider form battery, this is turned on by D0
// see http://fettricks.blogspot.co.nz/2014/01/reducing-voltage-divider-load-to-extend.html
void batteryMeasure() {
  digitalWrite(V_POWER, LOW);//close mosfet to measure
  delayMicroseconds(20); //wait for cap to discharge before reading
  //Serial.print("Value of measure pin is: ");
  int val = analogRead(V_PIN); //measure analog val for conversion
  //Serial.println(val);
  digitalWrite(V_POWER, HIGH);//open mosfet to conserve power
  //convert. Returns actual voltage, ie 3.768 = 3.768V
  voltage = (((float)val / 442) * 1.1) / (1.1 / 4.2);
}

void onReceive(int packetSize) {
  if (packetSize == 0) return;          // if there's no packet, return

  // read packet header bytes:
  //byte sender = LoRa.read();            // sender address

//  // if the recipient isn't this device or broadcast,
//  if (sender != ALLOWED) {
//    #ifdef debug
//      Serial.println("This message is not for me.");
//    #endif
//    return;                             // skip rest of function
//  }

  //otherwise build the string
  String incoming = "";

  while (LoRa.available()) {
    packet = LoRa.read()
    if ((packet == MAINTOP) or (packet == SALS) {
      #ifdef debug
        Serial.println("Deleting hex character");
      #endif
//      skipping
    }else{
      incoming += (char)LoRa.read();
    }
  }

  //forward the packet
  #ifdef debug
    Serial.print("Packet being forwarded is :");
    Serial.println(incoming);
  #endif
  LoRa.beginPacket();
  LoRa.write(tag);
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
  //send packet
  LoRa.beginPacket();
  LoRa.print("PY;");//tag for serial listner
  LoRa.print(NODE_ID);
  LoRa.print(";");
  //null value for relay
  LoRa.print("R");
  LoRa.print(";");
  LoRa.print(voltage);
  LoRa.print(";");
  LoRa.endPacket();
}

//external watchdog isr
void wake (){
  wake_resp = true;
}  // end of wake

void loop() {
  //send local data now and then
  if (millis() - send_timer > SEND_THRESH) {
    send_local_data();
    send_timer = millis();
  }
  if (wake_resp){
      //Send successful wake pulse to external watchdog
    digitalWrite(DONE, HIGH);
    delayMicroseconds(DONE_T);
    digitalWrite(DONE, LOW);
    wake_resp = false;
  }

  // parse for a packet, and call onReceive with the result:
  onReceive(LoRa.parsePacket());
}



