#include <SPI.h>
#include <LoRa.h>
long randNumber;
float v;
float volts;
int counter = 0;


void setup() {
  Serial.begin(9600);
  //while (!Serial);
  randomSeed(analogRead(0));

  Serial.println("LoRa Sender");
  LoRa.setPins(1, 4, 7);

  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
}

void loop() {
  LoRa.beginPacket();
  LoRa.print("Counter =  ");
  LoRa.print(counter);
  LoRa.endPacket();
  delay(10000);
  counter++;
  
  
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
