#include <Servo.h>

Servo myServo;

void setup() {
  Serial.begin(9600);
  myServo.attach(9);
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();  // Remove newline or whitespace

    int commaIndex = input.indexOf(',');
    if (commaIndex != -1) {
      int x = input.substring(0, commaIndex).toInt();
      int ln = input.substring(commaIndex + 1).toInt();

      x = constrain(x, 0, 640);               // Keep x in screen bounds
      int angle = map(x, 0, 640, 0, 180);     // Map x to servo angle

      if (ln > 30) {
        myServo.write(angle);                // Move servo only if hand is close enough
      }
    }
  }
}
