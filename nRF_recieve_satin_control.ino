#include <SPI.h>
#include <RF24.h>

RF24 radio(9, 10); // CE = pin 9, CSN = pin 10 — adjust if needed
const byte address[6] = "00001";  // Must match the transmitter

void setup() {
  Serial.begin(9600);
  radio.begin();

  radio.openReadingPipe(0, address);  // Open pipe 0 with the same address
  radio.setPALevel(RF24_PA_LOW);      // Adjust power level based on range needs
  radio.setDataRate(RF24_250KBPS);    // Optional: More reliable at long distances
  radio.startListening();             // Set module as receiver
}

void loop() {
  if (radio.available()) {
    int data[2];  // To store received x, y values

    radio.read(&data, sizeof(data));  // Read full data packet

    // Print received values to Serial Monitor
    Serial.print("Received X and Y: ");
    Serial.print(data[0]);
    Serial.print(" ");
    Serial.println(data[1]);
  }
}
