#include <Servo.h>

Servo myServo; // Create a servo object
int servoPin = 9; // Define the pin for servo motor control
int buttonPin = 2; // Define the pin for the button

void setup() {
  myServo.attach(servoPin); // Attach the servo to the specified pin
  pinMode(buttonPin, INPUT_PULLUP); // Set the button pin as input with internal pull-up resistor
}

void loop() {
  if (digitalRead(buttonPin) == LOW) { // Check if the button is pressed
    moveServo(); // Call function to move the servo
    delay(1000); // Debounce delay
  }
}

void moveServo() {
  myServo.write(90); // Rotate the servo to 90 degrees
  delay(2000); // Wait for 2 seconds (adjust as needed)
  myServo.write(0); // Return the servo to its initial position
}
