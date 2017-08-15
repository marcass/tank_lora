#include <SPI.h>
#include <LoRa.h>

#define debug

#define SS 1                  //NSS pin def for lora lib, use "1" for older modules and "8" for new modules (they have clearer text on ATMEL chip)
#define DIO  7               //DIO 0  for lora lib
#define RESET  4             //RESET pin for lora radio

void setup() {
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
    #ifdef debug
      // received a packet
      Serial.print("Received packet '");
    #endif

    // read packet
    while (LoRa.available()) {
      Serial.print((char)LoRa.read());
    }
    //make newline and carriage return for python parsing
    Serial.println();
    #ifdef debug
      // print RSSI of packet
      Serial.print("' with RSSI ");
      Serial.println(LoRa.packetRssi());
    #endif
  }
}


