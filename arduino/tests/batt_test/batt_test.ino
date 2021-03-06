#include <SPI.h>
#include <LoRa.h>
//Sonar stuff
//sleep stuff http://www.engblaze.com/hush-little-microprocessor-avr-and-arduino-sleep-mode-basics/
#include <avr/interrupt.h>
#include <avr/power.h>
#include <avr/sleep.h>
#include <avr/io.h>

//debug


float voltage;
#define V_measurePin 3
unsigned long timer;
unsigned long print_timer;
unsigned long PRINT_THRESH = 1000; //60000;
int val;

//power pin mosfet
#define POWER 5

void setup() {
  print_timer = millis();
  Serial.println("starting up");
  pinMode(POWER, OUTPUT);
  digitalWrite(POWER, HIGH);
  Serial.begin(9600);

    //.setup analog ref for battery testing
  analogReference(INTERNAL); //measures at 1.1V ref to give a value for flaoting voltage form batt
  Serial.println("LoRa Sender");
  LoRa.setPins(1, 4, 7);

  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
}

//battery testing function
//A3 connected to voltage divider form battery, this is turned on by D0
// see http://fettricks.blogspot.co.nz/2014/01/reducing-voltage-divider-load-to-extend.html
//specified voltage divider (3.74kOhnm high side and 10k to drain) gives a 4.2V down converted to 1.14V)

void batteryMeasure() {
  digitalWrite(POWER, LOW);//close mosfet to measure
  delay(1000);
  delayMicroseconds(20); //wait for cap to discharge before reading
  Serial.print("Value of measure pin is: ");
  val = analogRead(V_measurePin); //measure analog val for conversion
  Serial.println(val);
  digitalWrite(POWER, HIGH);//open mosfet to conserve power
  //convert. Returns actual voltage, ie 3.768 = 3.768V
  voltage = (((float)val / 442) * 1.1) / (1.1 / 4.2);
}


void loop() {

  if (millis() - print_timer > PRINT_THRESH){
    batteryMeasure();
//    Serial.print("battery voltage is ");
//    Serial.print(voltage);
//    Serial.println("V");
    LoRa.beginPacket();
    LoRa.print("PY;");
    LoRa.print("5;0;");
    LoRa.print(voltage);
    LoRa.print(";");
    LoRa.print(val);
    LoRa.endPacket();
    print_timer = millis();
  }
}



