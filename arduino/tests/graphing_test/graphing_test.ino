long randNumber;
float volts;
unsigned long SEND_INT = 150000;
unsigned long timer_start = 0;

void setup(){
  Serial.begin(9600);

  // if analog input pin 0 is unconnected, random analog
  // noise will cause the call to randomSeed() to generate
  // different seed numbers each time the sketch runs.
  // randomSeed() will then shuffle the random function.
  randomSeed(analogRead(0));
}

void send_data(){
  for(int x = 1; x < 5; x++) {
    // print a random number from 10 to 19
    randNumber = random(30, 70); // fake distances in cm
    volts = ((float)random(290, 420)/100);
    Serial.print("PY;");
    Serial.print(x);
    Serial.print(";");
    Serial.print(randNumber);
    Serial.print(";");
    Serial.print(volts);
    Serial.println(";");
  }
}

void loop() { 
  if (millis() - timer_start > SEND_INT) {
      send_data();
      timer_start = millis();
  }
  
}
