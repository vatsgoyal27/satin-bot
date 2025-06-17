#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

// Motor pins
const int IN1 = 2;
const int IN2 = 3;
const int IN3 = 4;
const int IN4 = 5;

RF24 radio(9, 10);  // CE, CSN
const byte address[6] = "00001";

// Struct definition must match sender
struct DataPacket {
  int x;
  int ln;
};

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  Serial.begin(9600);

  if (!radio.begin()) {
    while (1);  // Halt if radio fails
  }

  radio.setPALevel(RF24_PA_LOW);
  radio.setChannel(100);
  radio.openReadingPipe(0, address);
  radio.startListening();  // Set as receiver
}

void loop() {
  if (radio.available()) {
    DataPacket received;
    radio.read(&received, sizeof(received));

    int x = received.x;
    int ln = received.ln;

    if (ln < 100 && ln > 50) {
      if (x < 200) {
        // Move right
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
      } else if (x > 440) {
        // Move left
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
      } else {
        // Move forward
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
      }
    } else {
      // Stop
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, LOW);
    }
  }
}
