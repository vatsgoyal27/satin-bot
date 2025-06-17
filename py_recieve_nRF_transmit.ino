#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(9, 10);  // CE, CSN
const byte address[6] = "00001";

// Define a struct to hold x and ln
struct DataPacket {
  int x;
  int ln;
};

void setup() {
  Serial.begin(9600);
  if (!radio.begin()) {
    while (1);  // Halt if nRF24 fails
  }

  radio.setPALevel(RF24_PA_LOW);
  radio.setChannel(100);
  radio.openWritingPipe(address);
  radio.stopListening();  // Set as transmitter
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();  // remove newline or whitespace

    int commaIndex = input.indexOf(',');
    if (commaIndex != -1) {
      DataPacket data;
      data.x = input.substring(0, commaIndex).toInt();
      data.ln = input.substring(commaIndex + 1).toInt();

      radio.write(&data, sizeof(data));
    }
  }
}
