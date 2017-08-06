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
int V_measurePin = 1;
unsigned long timer;
unsigned long print_timer;
unsigned long PRINT_THRESH = 1000; //60000;

//power pin mosfet
const int POWER = 2;

void setup() {
  print_timer = millis();
  Serial.println("starting up");
  pinMode(POWER, OUTPUT);
  digitalWrite(POWER, HIGH);
  Serial.begin(9600);

    //.setup analog ref for battery testing
  analogReference(INTERNAL); //measures at 1.1V ref to give a value for flaoting voltage form batt
}

//battery testing function
//A3 connected to voltage divider form battery, this is turned on by D0
// see http://fettricks.blogspot.co.nz/2014/01/reducing-voltage-divider-load-to-extend.html
//specified voltage divider (3.74kOhnm high side and 10k to drain) gives a 4.2V down converted to 1.14V)

void batteryMeasure() {
  digitalWrite(POWER, LOW);//close mosfet to measure
  delayMicroseconds(20); //wait for cap to discharge before reading
  Serial.print("Value of measure pin is: ");
  int val = analogRead(V_measurePin); //measure analog val for conversion
  Serial.println(val);

  //delay(2);
  digitalWrite(POWER, HIGH);//open mosfet to conserve power
  //convert. Returns actual voltage, ie 3.768 = 3.768V
  voltage = (((float)val / 1024) * 1.1) / (1.1 / 4.2);
 
}


void loop() {

  if (millis() - print_timer > PRINT_THRESH){
    batteryMeasure();
    Serial.print("battery voltage is ");
    Serial.print(voltage);
    Serial.println("V");
    print_timer = millis();
  }
}



