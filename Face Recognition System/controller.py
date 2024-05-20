import serial
from pyfirmata import Arduino, util

# Define Arduino board port
PORT = "COM3"

# Initialize Arduino board
board = Arduino(PORT)

# LCD pins
rs = board.get_pin("a0")
en = board.get_pin("a1")
d4 = board.get_pin("a2")
d5 = board.get_pin("a3")
d6 = board.get_pin("a4")
d7 = board.get_pin("a5")

# Servo pin
servo_pin = 9

# Initialize LCD
from time import sleep
from pyfirmata import OUTPUT, HIGH, LOW

lcd = LiquidCrystal(rs, en, d4, d5, d6, d7)
lcd.begin(16, 2)

# Initialize servo
servo = board.get_pin("d:{}:s".format(servo_pin))

# Button pins
known_button_pin = 2
unknown_button_pin = 3

# Initialize button pins as input
board.digital[known_button_pin].mode = INPUT_PULLUP
board.digital[unknown_button_pin].mode = INPUT_PULLUP

# Open serial connection to communicate with Arduino
ser = serial.Serial(PORT, 9600)


# Function to rotate servo to a given angle
def rotate_servo(angle):
    servo.write(angle)


# Function to unlock the door
def unlock_door():
    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.print("Face recognized.")
    lcd.setCursor(0, 1)
    lcd.print("Door Unlocked")
    rotate_servo(90)  # Assuming 90 degree is unlocked position
    sleep(5)  # Wait for 5 seconds
    rotate_servo(0)  # Assuming 0 degree is initial position (locked)


# Function to handle unrecognized person
def unrecognized_person():
    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.print("Unrecognized")
    lcd.setCursor(0, 1)
    lcd.print("Person.")
    sleep(2)  # Display message for 2 seconds


# Main loop
while True:
    # Read state of push buttons
    known_pressed = not board.digital[known_button_pin].read()
    unknown_pressed = not board.digital[unknown_button_pin].read()

    # Check if face recognition buttons are pressed
    if known_pressed:
        unlock_door()
    elif unknown_pressed:
        unrecognized_person()
    else:
        # Display default message when no buttons are pressed
        lcd.clear()
        lcd.setCursor(0, 0)
        lcd.print("Please show face")
        lcd.setCursor(0, 1)
        lcd.print("to unlock door")
        sleep(0.5)
