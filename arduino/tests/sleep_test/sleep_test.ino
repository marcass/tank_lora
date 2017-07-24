/* TODO
 *  chjeck brownout and watrchdog is disables
 *  check that we can wake with ahigh level trigger (think it needs to be low according to datasheet
 *  set internal voltage level in getbandgap https://www.gammon.com.au/forum/?id=11497
 */  

#include <SPI.h>
#include <LoRa.h>
//Sonar stuff
#include <NewPing.h>
//sleep stuff http://www.engblaze.com/hush-little-microprocessor-avr-and-arduino-sleep-mode-basics/
#include <avr/interrupt.h>
#include <avr/power.h>
#include <avr/sleep.h>
#include <avr/io.h>

//#define sleeps
#define nosleep

int counter = 0;

//external watchdog
//wake pin on D2 (interrupt 0)
const byte wakepin = 2;

unsigned long timer;
unsigned long print_timer;
unsigned long PRINT_THRESH = 1000; //60000;
unsigned long last_gap;
unsigned long DONE_TIME = 20;
bool done_start = false;
const int DONE = 11;
unsigned long done_timer = 0;

//sleep pin
const int SLEEP_PIN = 3;


void setup() {
  pinMode(DONE, OUTPUT);
  digitalWrite(DONE, LOW);
  pinMode(wake, INPUT);
  //disable sleep bit:
  sleep_disable();
  pinMode(SLEEP_PIN, INPUT_PULLUP);
  
  Serial.begin(9600);

  Serial.println("LoRa Sender");
  LoRa.setPins(1, 4, 7); //reset is pd4, adc8, dio0 is P(ort)E 6 or int6

  if (!LoRa.begin(433E6)) { // initialise at 433MHz
    Serial.println("Starting LoRa failed!");
    while (1);
    
  }
}


void wake (){
  // cancel sleep as a precaution
  sleep_disable();
  // precautionary while we do other stuff
  detachInterrupt (digitalPinToInterrupt(wakepin));
  done_start = true;

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
  attachInterrupt (digitalPinToInterrupt(wakepin), wake, RISING);
  EIFR = bit (INTF0);  // clear flag for interrupt 0

  //to turn of BOD in hardware (fuses) use "avrdude <programmer> <chip> -U efuse:w:0xFE:m" see http://eleccelerator.com/fusecalc/fusecalc.php?chip=atmega32u4&LOW=62&HIGH=D9&EXTENDED=FF&LOCKBIT=FF
  
  // We are guaranteed that the sleep_cpu call will be done
  // as the processor executes the next instruction after
  // interrupts are turned on.
  interrupts ();  // one cycle
  sleep_cpu ();   // one cycle
}

void loop() {
  
    //delay(5000);
    if (!done_start){ //sleep if signal sent and watchdog had a done pulse
      //go to sleep when done
      //first check to see if we want to sleep (for testing/debugging purposes)
      if(digitalRead(SLEEP_PIN) == HIGH){ //Sleep mode enabled as it is pulled up when sleeping enabled
        Serial.print("Sleeping now. Had ");
        Serial.print(counter);
        Serial.println(" sleeps.");
        
        
        // send packet
        LoRa.beginPacket();
        LoRa.print("count = ");
        LoRa.print(counter);
        LoRa.endPacket();
      
        counter++;
        sleepNow();
      }else{
        Serial.println("Not sleeping");
        delay(3000);
      }
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



