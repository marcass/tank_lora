/* TODO
 *  set list of allowed nodes for forwarding
 *  test
 */  


#include <SPI.h>
#include <LoRa.h>
//Sonar stuff
//sleep stuff http://www.engblaze.com/hush-little-microprocessor-avr-and-arduino-sleep-mode-basics/
#include <avr/interrupt.h>
#include <avr/power.h>
#include <avr/sleep.h>
#include <avr/io.h>

//debug
#define debug

int counter = 0;
/*Assign node numbers
 * 1. Top tank
 * 2. Noels break
 * 2. Sal's bush
 */
const int NODE_ID = 1;
//allowed to forward for sals - more verstile than using syncword
int allowed_senders [] = {}//declare allowed address values here

#define SS 1                 //NSS pin def for lora lib
#define V_PIN  0             //measure voltage off this pin
#define POWER  3             //Power up n-channel mosfet to read distance
#define RESET  4             //RESET pin for lora radio
#define V_POWER 5            //pull down p-channel mosfet to measure voltage
#define DIO  7               //DIO 0  for lora lib
#define TRIGPIN  11          // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHOPIN     12       // Arduino pin tied to echo pin on the ultrasonic sensor.


float voltage;
unsigned long send_timer;
const unsigned long SEND_THRESH = 1500000; //25min

//LoRa radio setup https://github.com/sandeepmistry/arduino-LoRa/blob/master/API.md
//Lower number if closer receiver (saves power)
//LoRa.setTxPower(txPower); //Supported values are between 2 and 17 for PA_OUTPUT_PA_BOOST_PIN, 0 and 14 for PA_OUTPUT_RFO_PIN.

void setup() {
  send_timer = millis();
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

//measrue distance to water
void distMeasure(){
  digitalWrite(POWER, HIGH);
  delay(350); //measured as nneding to be above 280ms for saturation of boost converter
  digitalWrite(TRIGPIN, LOW); // Set the trigger pin to low for 2uS
  delayMicroseconds(2);
  digitalWrite(TRIGPIN, HIGH); // Send a 10uS high to trigger ranging
  delayMicroseconds(10);
  digitalWrite(TRIGPIN, LOW); // Send pin low again
  int distance = pulseIn(ECHOPIN, HIGH,26000); // Read in times pulse
  distance= distance/58;
  #ifdef debug
    Serial.print(distance);
    Serial.println("   cm");                    
  #endif
}

void onReceive(int packetSize) {
  if (packetSize == 0) return;          // if there's no packet, return

  // read packet header bytes:
  byte sender = LoRa.read();            // sender address

  String incoming = "";

  while (LoRa.available()) {
    incoming += (char)LoRa.read();
  }

  // if the recipient isn't this device or broadcast,
  if (sender != 0xFF) {
    #ifdef debug
      Serial.println("This message is not for me.");
    #endif
    return;                             // skip rest of function
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

  // parse for a packet, and call onReceive with the result:
  onReceive(LoRa.parsePacket());
}



