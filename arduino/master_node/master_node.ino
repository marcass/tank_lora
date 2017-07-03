#include <SPI.h>
#include <LoRa.h>

#define debug
//#define production
//#define noncallback
#define callback

int payload;

//initialise mycontroller to await sensor info
const int TOP = 1;
const int NOEL = 2;
const int SAL = 3;
const int SENS = 3; //nuber of sensors for for loop
int node_id;
// presentation described here: https://www.mysensors.org/download/serial_api_20
String present = ";1;0;0;15";



void setup() {
  Serial.begin(9600);
  #ifdef production
    //present sensors to MyController
    int sensors[] = {TOP, NOEL, SAL};
    for (int n = 0; n < SENS; n++) {
      node_id = sensors[n];
      String present_node = (node_id + present);
      Serial.println(present_node);
    }
  #endif
    
  while (!Serial);

  Serial.println("LoRa Receiver");
  LoRa.setPins(1, 4, 7);

  if (!LoRa.begin(433E6)) { // initialise at 433MHz
    Serial.println("Starting LoRa failed!");
    while (1);
  }

  #ifdef callback
    // register the receive callback
    LoRa.onReceive(onReceive);
  
    // put the radio into receive mode
    LoRa.receive();
  #endif
}

void loop() {
  #ifdef noncallback
    // try to parse packet
    int packetSize = LoRa.parsePacket();
    if (packetSize) {
      // received a packet
      #ifdef debug
        Serial.print("Received packet '");
    
        // read packet
        while (LoRa.available()) {
          Serial.print((char)LoRa.read());
        }
    
        // print RSSI of packet
        Serial.print("' with RSSI ");
        Serial.println(LoRa.packetRssi());
      #endif debug
  
      #ifdef production
        // read packet parsed at node in my controller format and print to serial for API
        while (LoRa.available()) {
          Serial.print((char)LoRa.read());
        }
      #endif
  }
  #endif
}

//call back fucntion may be able to sleep mcu and wake with tx pin activity in callback
void onReceive(int packetSize) {
  // received a packet
  Serial.print("Received packet '");

  // read packet
  for (int i = 0; i < packetSize; i++) {
    Serial.print((char)LoRa.read());
  }

  // print RSSI of packet
  Serial.print("' with RSSI ");
  Serial.println(LoRa.packetRssi());
}

