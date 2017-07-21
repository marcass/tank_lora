long randNumber;
unsigned long interval;
float volts;
unsigned long timer_start = 0;
int tank = 1;

void setup(){
  Serial.begin(9600);

  // if analog input pin 0 is unconnected, random analog
  // noise will cause the call to randomSeed() to generate
  // different seed numbers each time the sketch runs.
  // randomSeed() will then shuffle the random function.
  randomSeed(analogRead(0));
}

void compose_msg(){
  randNumber = random(30, 100); // fake distances in cm
  volts = ((float)random(290, 420)/100);
  Serial.print("PY;");
  Serial.print(tank);
  Serial.print(";");
  Serial.print(randNumber);
  Serial.print(";");
  Serial.print(volts);
  Serial.println(";");
  interval = random(120000, 1800000); //generate random interval for next publish between 2 and 30 min
}

void loop() { 
  if (millis() - timer_start > interval) {
    compose_msg();
    if (tank >= 3){
      tank = 1;
    }else{
      tank++;
    }
    timer_start = millis();
  }
  
}
