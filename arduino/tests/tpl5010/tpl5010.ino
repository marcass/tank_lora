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
//#define sensor
//#define mycontroller
//#define python
//#define sleeps


int counter = 0;
int sensor_node = 1;

//external watchdog
//wake pin on D2 (interrupt 0)
const int DONE = 11;
unsigned long done_timer = 0;
bool intitialisePins;
float voltage;
int V_measurePin = 0;
bool pulse = false;
unsigned long gap;
const byte interruptPin = 2;
unsigned long timer;
unsigned long print_timer;
unsigned long PRINT_THRESH = 1000; //60000;
unsigned long last_gap;
unsigned long DONE_TIME = 20;
bool done_start = false;

//sleep pin
const int SLEEP_PIN = 1;
//power pin for u/s module (can't power directly as 10mA limit and need 30mA, so using step up/mosfet)
const int POWER = 6;

void setup() {
  print_timer = millis();
  pinMode(interruptPin, INPUT);
  Serial.println("starting up");
  //disable sleep bit:
  sleep_disable();
  pinMode(DONE, OUTPUT);
  digitalWrite(DONE, LOW);
  pinMode(POWER, OUTPUT);
  digitalWrite(POWER, LOW);
  pinMode(SLEEP_PIN, INPUT_PULLUP);
  //tpl510 testing
  attachInterrupt(digitalPinToInterrupt(interruptPin), heartbeat, RISING);
 
  Serial.begin(9600);
  //while (!Serial); //uncomment to require serial connection to work
  gap = millis();
  Serial.println("LoRa Sender");
  LoRa.setPins(1, 4, 7); //reset is pd4, adc8, dio0 is P(ort)E 6 or int6

  if (!LoRa.begin(433E6)) { // initialise at 433MHz
    Serial.println("Starting LoRa failed!");
    while (1);
  }
//  //.setup analog ref for battery testing
//  analogReference(INTERNAL); //measures at 1.1V ref to give a value for flaoting voltage form batt
//  //initialise measurement pin
//  pinMode(V_measurePin, OUTPUT);
//  digitalWrite(V_measurePin, HIGH);
}

//battery testing function
//A3 connected to voltage divider form battery, this is turned on by D0
// see http://fettricks.blogspot.co.nz/2014/01/reducing-voltage-divider-load-to-extend.html
//specified voltage divider (3.74kOhnm high side and 10k to drain) gives a 4.2V down converted to 1.14V)

void batteryMeasure() {
  digitalWrite(V_measurePin, LOW);//close mosfet to measure
  delayMicroseconds(100); //wait for cap to discharge before reading
  float val = analogRead(3); //measure analog val for conversion
  digitalWrite(V_measurePin, HIGH);//open mosfet to conserve power
  //convert. Returns actual voltage, ie 3.768 = 3.768V
  voltage = (val / 1024) / 1024 * 4.2;

  
}


//Tpl5010 isr
void heartbeat(){
  pulse = true;
  detachInterrupt(0);
  last_gap = (millis() - gap)/1000;
}
void wake (){
  // cancel sleep as a precaution
  sleep_disable();
  // precautionary while we do other stuff
  detachInterrupt (0);
  //set wake flag to process pins
  intitialisePins = true;
}  // end of wake

void sleepNow(){ //see https://www.gammon.com.au/forum/?id=11497

  //sleep lora radio
  LoRa.sleep();
  
  // Choose our preferred sleep mode:
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  
  // disable ADC
  ADCSRA = 0;
  
  //power_all_disable();//disables power to all modules careful here as not sure how to wake up
  // Set sleep enable (SE) bit:
  sleep_enable();

  //set pins for low power
  
  
  // Do not interrupt before we go to sleep, or the
  // ISR will detach interrupts and we won't wake.
  noInterrupts ();           // timed sequence follows
  
  // will be called when pin D2 goes high  
  attachInterrupt (0, wake, RISING);
  EIFR = bit (INTF0);  // clear flag for interrupt 0

  //to turn of BOD in hardware (fuses) use "avrdude <programmer> <chip> -U efuse:w:0xFE:m" see http://eleccelerator.com/fusecalc/fusecalc.php?chip=atmega32u4&LOW=62&HIGH=D9&EXTENDED=FF&LOCKBIT=FF
  
  // We are guaranteed that the sleep_cpu call will be done
  // as the processor executes the next instruction after
  // interrupts are turned on.
  interrupts ();  // one cycle
  sleep_cpu ();   // one cycle
}

void loop() {
  
  if(pulse){
    gap = millis();
    // send packet
    LoRa.beginPacket();
    LoRa.print("NodeID ");
    LoRa.print(sensor_node);
    LoRa.print("count ");
    LoRa.print(counter);
    LoRa.endPacket();
    //send done
    Serial.println("sending done");
    digitalWrite(DONE, HIGH);
    delay(15);
    digitalWrite(DONE, LOW);
    attachInterrupt(0, heartbeat, RISING);
  
    counter++;
    pulse = false;
    done_start = true;
    
    
    
  }
  timer = (millis() - gap)/1000;
  if (millis() - print_timer > PRINT_THRESH){
    //timer = (millis() - gap)/1000;
    Serial.print("This many wakes: ");
    Serial.print(counter);
    Serial.print(" Time gap = ");
    Serial.print(timer);

    Serial.print("s, = ");
    Serial.print(timer/60);
    Serial.print("min. Last gap was: ");
    Serial.print(last_gap);
    Serial.print("s, = ");
    Serial.print(last_gap/60);
    Serial.println("min");
    print_timer = millis();
  }

  //Send successful wake pulse to external watchdog
  if (done_start){
    if (done_timer == 0){
      digitalWrite(DONE, HIGH);
      done_timer = millis();
    }
  }
  if ((millis() - done_timer) > DONE_TIME){
    digitalWrite(DONE, LOW);
    done_timer = 0;
    done_start = false;
  }

}



