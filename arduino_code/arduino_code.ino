int altitude = 10;
int temperature = 30;
int velocity = 5;
int pressure = 1;
int duration = 0;

void setup() {

  Serial.begin(9600);

}

void loop() {

    duration = duration + 1;
    altitude = altitude + rand();
    temperature = temperature + rand();
    velocity = velocity + rand();
    pressure = pressure + rand();

  Serial.print(altitude);
  Serial.print(",");
  Serial.print(temperature);
  Serial.print(",");
  Serial.print(velocity);
  Serial.print(",");
  Serial.print(pressure);   
  Serial.print(",");
  Serial.println(duration);         // println()  To finish the code
  
  delay(1000);

}
