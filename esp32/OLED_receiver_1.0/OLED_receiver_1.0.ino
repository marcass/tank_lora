/*
 * Ensure TTGO LORA32-OLED V1 board selected
 * Process goes:
 * - capture data
 * - forward to api
 * - disply onsite data on OLED for Rob
 * - display time since last message
 */

#include <Wire.h>  // Only needed for Arduino 1.6.5 and earlier
//needs this lib https://github.com/ThingPulse/esp8266-oled-ssd1306 (daniel somethig in libs for arduino)
#include "SSD1306.h"

#include <SPI.h>
#include <LoRa.h>

// (something, SDA, SCL), see
//https://github.com/LilyGO/TTGO-LORA32-V2.0/issues/3
SSD1306 display(0x3c, 21, 22);

#define SS 18
#define RST 23
#define DI0 26

// LoRa Settings (these a lib defaults)
#define BAND 433E6
#define spreadingFactor 7
#define SignalBandwidth 125E3

#define codingRateDenominator 8

//timers
unsigned long new_rec;
unsigned long old_rec;
  
void setup() {
  pinMode(16,OUTPUT);
  digitalWrite(16, LOW); // set GPIO16 low to reset OLED
  delay(50);
  digitalWrite(16, HIGH);

  display.init();
  display.flipScreenVertically();
  display.setFont(ArialMT_Plain_10);
  display.setTextAlignment(TEXT_ALIGN_LEFT);
  
  Serial.begin(115200);
//  while (!Serial); //if just the the basic function, must connect to a computer
  delay(1000);
  
  Serial.println("LoRa Receiver");
  display.drawString(5,5,"LoRa Receiver");
  display.display();
  SPI.begin(5,19,27,18);
  LoRa.setPins(SS,RST,DI0);

  if (!LoRa.begin(BAND)) {
    display.drawString(5,25,"Starting LoRa failed. Kill a kitten");
    while (1);
  }
  Serial.println("LoRa Initialised. Pat a kitten");
  
  Serial.print("LoRa Frequency: ");
  Serial.println(BAND);
  
  Serial.print("LoRa Spreading Factor: ");
  Serial.println(spreadingFactor);
  LoRa.setSpreadingFactor(spreadingFactor);
  
  Serial.print("LoRa Signal Bandwidth: ");
  Serial.println(SignalBandwidth);
  LoRa.setSignalBandwidth(SignalBandwidth);

  LoRa.setCodingRate4(codingRateDenominator);
  
  display.drawString(5,25,"LoRa Initializing OK!");
  display.display();
  new_rec = millis();
  old_rec = millis();
}

void loop() {
  // try to parse packet
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    old_rec = new_rec;
    new_rec = millis();
    // received a packet
    Serial.print("Received packet. ");
    
    display.clear();
    display.setFont(ArialMT_Plain_16);
    display.drawString(3, 0, "Received packet ");
    display.display();
    
    // read packet
    while (LoRa.available()) {
      String data = LoRa.readString();
      Serial.print(data);
      display.drawString(20,22, data);
      display.display();
    }
    
    // print RSSI of packet
    Serial.print(" with RSSI ");
    Serial.println(LoRa.packetRssi());
    Serial.print(" with SNR ");
    Serial.println(LoRa.packetSnr());
    // display.drawString(0, 45, "RSSI: ");
    // display.drawString(50, 45, (String)LoRa.packetRssi());
    
//    display.drawString(0, 45, (String)LoRa.packetRssi() + "dB (" + (String)LoRa.packetSnr() +"dB)");
    Serial.print("Old time ");
    Serial.println(old_rec);
    Serial.print("New time ");
    Serial.println(new_rec);
    unsigned long gap = (new_rec - old_rec)/1000;
    Serial.print("Gap is this many seconds: ");
    Serial.println(gap);
    int minutes = gap/60;
    Serial.print("Minutes: ");
    Serial.println(minutes);
    int seconds = gap % 60;
    Serial.print("Seconds: ");
    Serial.println(seconds);
    display.drawString(0, 45, "Gap "+(String)minutes + "m, "+(String)seconds +"s");
        
    display.display();
  }
}
