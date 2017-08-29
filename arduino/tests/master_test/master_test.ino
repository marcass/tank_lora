#include <SPI.h>
#include <LoRa.h>

#define debug

#define SS 8                  //NSS pin def for lora lib, use "1" for older modules and "8" for new modules (they have clearer text on ATMEL chip)
#define DIO  7               //DIO 0  for lora lib
#define RESET  4             //RESET pin for lora radio
#define LED 13               //led for blinking on message receipt

unsigned long blink_timer = 0;
const unsigned long THRESH = 500;
bool blink_led = false;
String output_str = "";
int nodeID;
String NODES[] = {"top", "noels", "sals", "bay", "main"};
int counter[] = {0,0,0,0,0};

void setup() {
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
  Serial.begin(9600);
  //while (!Serial);

  //Serial.println("LoRa Receiver");
  LoRa.setPins(SS, RESET, DIO); 

  if (!LoRa.begin(433E6)) { // initialise at 433MHz
    #ifdef debug
      Serial.println("Starting LoRa failed!");
    #endif
    while (1);
  }
}

void loop() {
  // try to parse packet
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    blink_led = true;
    #ifdef debug
      // received a packet
      Serial.print("Received packet '");
    #endif

    // read packet
    while (LoRa.available()) {
      //get the new byte
      char inChar = (char)LoRa.read();
      output_str += inChar;
    }
    //make newline and carriage return for python parsing
    Serial.println(output_str);
    #ifdef debug
      String in_node = getValue(output_str, ';', 1);
      //adjust for array being zero indexed
      nodeID = int(in_node) - 1;
      counter[nodeID] + 1;
      // print RSSI of packet
      Serial.print(NODES[nodeID]);
      Serial.print(" received = ");
      Serial.print(counter[nodeID]);
      Serial.print(" with RSSI ");
      Serial.println(LoRa.packetRssi());
    #endif
  }
  output_str = "";
  //blink on package receipt
  if (blink_led){
    if (blink_timer == 0){
      digitalWrite(LED, HIGH);
      blink_timer = millis();
    }
    if (millis() - blink_timer > THRESH){
      digitalWrite(LED, LOW);
      blink_timer = 0;
      blink_led = false;
    }
  }
}


