long randNumber;

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
    Serial.print("PYTHON;");
    Serial.print(x);
    Serial.print(";");
    Serial.print(randNumber);
    Serial.print(";");
    Serial.println("");

    delay(20000);
  }
}

void loop() { 
  send_data();
  
}
