#include <SPI.h>
#include <LoRa.h>
long randNumber;
float v;
float volts;
int counter = 0;
byte destination = 0xFF;


void setup() {
  delay(7000);
  Serial.begin(115200);
  //while (!Serial);
//  randomSeed(analogRead(0));

  Serial.println("LoRa Sender");
  LoRa.setPins(1, 4, 7);
//  LoRa.setPins(8, 4, 7);

  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
}

void loop() {
  LoRa.beginPacket();
  LoRa.write(destination);
  LoRa.print("PY;5;201;3.20;");
  LoRa.endPacket();
  delay(10000);
  counter++;
  Serial.println("sending");
  
  
//  for(int x = 1; x < 5; x++) {
//    // print a random number for water level
//    randNumber = random(30, 70); // fake distances in cm
//    v = random(290, 420);
//    volts = v/100;
//    LoRa.beginPacket();
//    LoRa.print("PY;");
//    LoRa.print(x);
//    LoRa.print(";");
//    LoRa.print(randNumber);
//    LoRa.print(";");
//    LoRa.print(volts);
//    LoRa.println(";");
//    LoRa.endPacket();
//    delay(5000);
//  }
}
