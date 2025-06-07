#include <SPI.h>
#include <RF24.h>

RF24 radio(9, 10); // CE = pin 9, CSN = pin 10

const byte address[6] = "00001";  // 5-byte address (must match receiver)

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.openWritingPipe(address);     // Set TX address
  radio.setPALevel(RF24_PA_LOW);      // Use low power for testing (change as needed)
  radio.setDataRate(RF24_250KBPS);    // Optional: more reliable over distance
  radio.stopListening();              // Set module as transmitter
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');  // Read full line from Python
    int commaIndex = input.indexOf(',');

    if (commaIndex > 0) {
      int x = input.substring(0, commaIndex).toInt();
      int y = input.substring(commaIndex + 1).toInt();

      // Offset to center (0,0) if needed
      int data[2] = {x - 320, y - 240};

      // Transmit over nRF
      bool success = radio.write(&data, sizeof(data));

      // Print debug info
      Serial.print("Sent X: "); Serial.print(x);
      Serial.print(" Y: "); Serial.print(y);
      Serial.println(success ? " ✓" : " ✗");
    }
  }
}
