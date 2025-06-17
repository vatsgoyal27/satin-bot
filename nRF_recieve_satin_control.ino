#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

// nRF24L01 setup
RF24 radio(9, 10);  // CE, CSN
const byte address[6] = "00001";

// Motor A
const int IN1 = 2;
const int IN2 = 3;
const int ENA = 6;

// Motor B
const int IN3 = 4;
const int IN4 = 7;
const int ENB = 5;

int speedA = 100;
int speedB = 100;

// Data packet structure (only x)
struct DataPacket {
  int x;
};

DataPacket receivedData;

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);

  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);

  if (!radio.begin()) {
    while (1);  // Halt if radio not found
  }

  radio.setPALevel(RF24_PA_LOW);
  radio.setChannel(100);
  radio.openReadingPipe(0, address);
  radio.startListening();
}

// Movement functions
void forward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, speedA);
  analogWrite(ENB, speedB);
}

void left() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, speedA);
  analogWrite(ENB, 0);
}

void right() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, 0);
  analogWrite(ENB, speedB);
}

void stopMotors() {
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

void loop() {
  if (radio.available()) {
    radio.read(&receivedData, sizeof(receivedData));
    int x = receivedData.x;

    // Movement decisions based on x value
    if (x < 213) {
      left();
    } else if (x > 426) {
      right();
    } else {
      forward();
    }
  }

  delay(50);  // Adjust as needed for smoother control
}
