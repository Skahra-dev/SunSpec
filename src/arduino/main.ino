void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char incomingByte = Serial.read();
    Serial.print("Received: ");
    Serial.println(incomingByte);
  }
}
