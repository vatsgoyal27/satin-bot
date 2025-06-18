#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(9, 10);  // CE, CSN
const byte address[6] = "00001";

// Structure to hold just one int: x
struct DataPacket {
  int x;
};

void setup() {
  Serial.begin(9600);

  if (!radio.begin()) {
    while (1);  // Stop if radio doesn't initialize
  }

  radio.setPALevel(RF24_PA_LOW);
  radio.setChannel(100);
  radio.openWritingPipe(address);
  radio.stopListening();  // Set as transmitter
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();  // remove whitespace/newlines

    if (input.length() > 0) {
      DataPacket data;
      data.x = input.toInt();  // convert string to int

      radio.write(&data, sizeof(data));
    }
  }
}
