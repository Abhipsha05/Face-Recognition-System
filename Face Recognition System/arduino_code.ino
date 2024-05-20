#include <Servo.h>
#include <LiquidCrystal.h>

// Define LCD connections
const int rs = A0, en = A1, d4 = A2, d5 = A3, d6 = A4, d7 = A5;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// Define servo motor pin
const int servoPin = 9;
Servo servo;

// Define push button pins
const int knownButtonPin = 2;
const int unknownButtonPin = 3;

bool doorLocked = true;

void setup() {
  // Initialize LCD
  lcd.begin(16, 2);

  // Initialize servo motor
  servo.attach(servoPin);
  // Move servo to initial position (locked)
  servo.write(0); // Assuming 0 degree is initial position (locked)

  // Initialize push buttons
  pinMode(knownButtonPin, INPUT_PULLUP);
  pinMode(unknownButtonPin, INPUT_PULLUP);

  // Initialize serial communication
  Serial.begin(9600);
}

void loop() {
  // Read state of push buttons
  bool knownPressed = digitalRead(knownButtonPin) == LOW;
  bool unknownPressed = digitalRead(unknownButtonPin) == LOW;

  // Check if face recognition buttons are pressed
  if (knownPressed) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Face recognized.");
    lcd.setCursor(0, 1);
    lcd.print("Door Unlocked");
    //delay(2000); // Display message for 2 seconds
    // Move servo to unlock position
    servo.write(90); // Assuming 90 degree is unlocked position
    delay(5000); // Wait for 2 seconds
    // Move servo back to initial position (locked)
    servo.write(0); // Assuming 0 degree is initial position (locked)
  } else if (unknownPressed) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Unrecognized");
    lcd.setCursor(0, 1);
    lcd.print("Person.");
    delay(2000); // Display message for 2 seconds
  } else {
    // Display default message when no buttons are pressed
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Please show face");
    lcd.setCursor(0, 1);
    lcd.print("to unlock door");
    delay(500);
  }
}
