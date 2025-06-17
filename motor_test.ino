// Motor A
const int IN1 = 2;
const int IN2 = 3;
const int ENA = 6;  // PWM for Motor A

// Motor B
const int IN3 = 4;
const int IN4 = 7;
const int ENB = 5;  // PWM for Motor B

// Speed setting (0–255)
int speedA = 100;
int speedB = 100;

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);

  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);

  Serial.begin(9600);
}

// Move both motors forward
void forward() {
  Serial.println("Moving FORWARD");
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, speedA);
  analogWrite(ENB, speedB);
}

// Move both motors backward
void backward() {
  Serial.println("Moving BACKWARD");
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, speedA);
  analogWrite(ENB, speedB);
}

// Turn right (stop right motor, run left motor)
void right() {
  Serial.println("Turning RIGHT");
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, 0);
  analogWrite(ENB, speedB);
}

// Turn left (run right motor, stop left motor)
void left() {
  Serial.println("Turning LEFT");
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, speedA);
  analogWrite(ENB, 0);
}

// Stop both motors
void stopMotors() {
  Serial.println("Motors STOPPED");
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

void loop() {
  forward();
  delay(2000);

  backward();
  delay(2000);

  left();
  delay(1500);

  right();
  delay(1500);

  stopMotors();
  delay(2000);
}

