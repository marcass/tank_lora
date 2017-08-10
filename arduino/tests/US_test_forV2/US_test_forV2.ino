#define ECHOPIN 12// Pin to receive echo pulse
#define TRIGPIN 11// Pin to send trigger pulse
void setup(){
  Serial.begin(9600);
  //pinMode(ECHOPIN, INPUT);
  pinMode(TRIGPIN, OUTPUT);
  //digitalWrite(ECHOPIN, HIGH);
  pinMode(ECHOPIN, INPUT_PULLUP);
}
void loop(){
  digitalWrite(TRIGPIN, LOW); // Set the trigger pin to low for 2uS
  delayMicroseconds(2);
  digitalWrite(TRIGPIN, HIGH); // Send a 10uS high to trigger ranging
  delayMicroseconds(10);
  digitalWrite(TRIGPIN, LOW); // Send pin low again
  int distance = pulseIn(ECHOPIN, HIGH,26000); // Read in times pulse
  distance= distance/58;
  Serial.print(distance);
  Serial.println("   cm");                    
  delay(50);// Wait 50mS before next ranging
}
