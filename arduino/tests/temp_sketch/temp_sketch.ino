 // Internal Temperature Sensor
// Example sketch for ATmega328 types.
// 
// April 2012, Arduino 1.0

void setup()
{
  Serial.begin(9600);
  ADMUX = 0;
  ADMUX |= (1 << REFS1);
  ADMUX |= (1 << REFS0);
  ADMUX |= (0 << MUX4);
  ADMUX |= (0 << MUX3);
  ADMUX |= (1 << MUX2); //preceding and folling lines inlc this one for ADC on nano
  ADMUX |= (1 << MUX1);
  ADMUX |= (1 << MUX0);

  //delay(20);            // wait for voltages to become stable.
  ADCSRA = 0;
  ADCSRA |= (1 << ADEN); 
  ADCSRA |= (1 << ADPS2);

  ADCSRB = 0;
  ADCSRB |= (1 << MUX5); 
  Serial.println(F("Internal Temperature Sensor"));
}

void loop(){

  Serial.print("Time: ");
  Serial.print(millis());
  Serial.print(" Core Temperature: ");
  Serial.print(getTemp());
  Serial.println(" C");

  delay(1000);
}


int getTemp(){
  ADCSRA |= (1 << ADSC);  //Start temperature conversion
  while (bit_is_set(ADCSRA, ADSC));  //Wait for conversion to finish
  byte low  = ADCL;
  byte high = ADCH;
  int temperature = (high << 8) | low;  //Result is in kelvin
  return temperature - 273;
}

