long randNumber;
float volts;

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
    Serial.print(";1;"); //marker for water level
    Serial.print(randNumber);
    Serial.print(";");
    Serial.println("");
    volts = (random(290, 420)/100)
    Serial.print("PYTHON;");
    Serial.print(x);
    Serial.print(";0;"); //marker for battery status
    Serial.print(volts);
    Serial.print(";");
    Serial.println("");    

    delay(10);
  }
}

void loop() { 
  send_data();
  delay(130000);//delay for just over 2min for sending 8 sets of data
  
}
