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
  radio.openReadingPipe(0, address);
  radio.startListening();

  Serial.println("Receiver ready");
}

void loop() {
  if (radio.available()) {
    int x;
    radio.read(&x, sizeof(x));

    Serial.print("Received x: ");
    Serial.println(x);

    if (x > 320) {
      //do something
    } else {
      //do something else
    }
  }
}
