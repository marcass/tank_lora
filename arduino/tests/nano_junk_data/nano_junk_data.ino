// Genearte random data for testing docker 

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
  int i;
  for (i = 0; i < 7; i++) {
    float voltage = random(300, 500);
    float volts = voltage/100;
    int level = random(30, 250);
    Serial.print("PY;");
    Serial.print(i);
    Serial.print(";");
    Serial.print(level);
    Serial.print(";");
    Serial.print(volts);
    Serial.println(";");
    delay(7000);
  }
}



