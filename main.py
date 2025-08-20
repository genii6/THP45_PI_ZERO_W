import RPi.GPIO as GPIO
import time

BUTTON_GPIO = 17  # Change this to your actual pin number

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO, GPIO.OUT)

# Default = button not pressed
GPIO.output(BUTTON_GPIO, GPIO.LOW)

# Simulate a press
GPIO.output(BUTTON_GPIO, GPIO.HIGH)
time.sleep(0.2)  # hold for 200ms
GPIO.output(BUTTON_GPIO, GPIO.LOW)
GPIO.cleanup()