
#include <SPI.h>
#include <LoRa.h>
#include <avr/interrupt.h>
#include <NewPing.h>

#define POWER 3
#define TRIGGER_PIN  12  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     11  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 200 
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

int counter = 0;
int dist;

void setup() {
  Serial.begin(9600);
  pinMode(POWER, OUTPUT);
  digitalWrite(POWER, LOW);
  Serial.println("LoRa Sender");
  LoRa.setPins(1, 4, 7); //reset is pd4, adc8, dio0 is P(ort)E 6 or int6

  if (!LoRa.begin(433E6)) { // initialise at 433MHz
    Serial.println("Starting LoRa failed!");
    while (1);
    //record current state of analogue read pins
    
    
  }
  pinMode(ECHO_PIN, INPUT_PULLUP);
}

void loop() {
  delay(3000);
  //READ MESSAGE
  digitalWrite(POWER, HIGH);
  delay(3000);
  dist = sonar.ping_cm();
  digitalWrite(POWER, LOW);
  // send packet
//  LoRa.beginPacket();
//  LoRa.print("Ping = ");
//  LoRa.print(sonar.ping_cm());
//  LoRa.print("cm");  
//  LoRa.print(": count = ");
//  LoRa.print(counter);
//  LoRa.endPacket();

  Serial.print("Ping = ");
  Serial.print(sonar.ping_cm());
  Serial.print("cm");  
  Serial.print(": count = ");
  Serial.println(counter);

  counter++;
}



