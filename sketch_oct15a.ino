#include <Servo.h>

Servo myServo;  // Create servo object
int servoPin = 9;  // Pin connected to the servo signal wire
int servoPos = 90;  // Initial servo position (center)
String receivedData = "";  // Variable to store serial input

void setup() {
  Serial.begin(9600);  // Start serial communication
  myServo.attach(servoPin);  // Attach servo to pin
  myServo.write(servoPos);  // Set initial position to 90 degrees
}

void loop() {
  // Check if data is available on the serial port
  if (Serial.available() > 0) {
    char incomingByte = Serial.read();  // Read the incoming byte

    // If a newline character is received, process the complete string
    if (incomingByte == '\n') {
      float faceOffset = receivedData.toFloat();  // Convert the received string to float

      // Map the face offset (-100 to 100) to servo position (0 to 180)
      servoPos = map(faceOffset, -100, 100, 0, 180);
      
      // Constrain the servo position within bounds (0 to 180 degrees)
      servoPos = constrain(servoPos, 0, 180);

      // Move the servo to the calculated position
      myServo.write(servoPos);

      // Clear the received data for the next input
      receivedData = "";
    } else {
      // If it's not a newline, keep adding the characters to the string
      receivedData += incomingByte;
    }
  }
}
