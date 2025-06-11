#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(9, 10);  // CE, CSN
const byte address[6] = "00001";

void setup() {
  Serial.begin(9600);
  if (!radio.begin()) {
    Serial.println("nRF24 not responding");
    while (1);
  }

  radio.setPALevel(RF24_PA_LOW);
  radio.setChannel(100);
  radio.openWritingPipe(address);
  radio.stopListening();
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
      int x = input.toInt();
      // You can clamp or map x if needed

      bool ok = radio.write(&x, sizeof(x));
    }
  }

