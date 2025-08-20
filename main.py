import RPi.GPIO as GPIO
import time
import sqlite3

BUTTON_GPIO_UP = 22
BUTTON_GPIO_DOWN = 27
BUTTON_GPIO_ENTER = 22

BUTTON_LONG_PRESS_DURATION = 3.0  # 3000ms
BUTTON_SHORT_PRESS_DURATION = 0.2  # 200ms
PAUSE_DURATION = 1  # 1 second

THP45_DB = 'THP45.db'

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO_UP, GPIO.OUT)
    GPIO.setup(BUTTON_GPIO_DOWN, GPIO.OUT)
    GPIO.setup(BUTTON_GPIO_ENTER, GPIO.OUT)
    # Default = buttons not pressed
    GPIO.output(BUTTON_GPIO_UP, GPIO.LOW)
    GPIO.output(BUTTON_GPIO_DOWN, GPIO.LOW)
    GPIO.output(BUTTON_GPIO_ENTER, GPIO.LOW)

def short_press(pin):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(BUTTON_SHORT_PRESS_DURATION)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(PAUSE_DURATION)

def simulate_setup_mode():
    # Simulate a long press to enter setup mode
    GPIO.output(BUTTON_GPIO_UP, GPIO.HIGH)
    GPIO.output(BUTTON_GPIO_DOWN, GPIO.HIGH)
    time.sleep(BUTTON_LONG_PRESS_DURATION)
    GPIO.output(BUTTON_GPIO_UP, GPIO.LOW)
    GPIO.output(BUTTON_GPIO_DOWN, GPIO.LOW)
    time.sleep(PAUSE_DURATION)

def enter_blockout_mode():
    # Simulate a short press to enter blockout mode
    short_press(BUTTON_GPIO_DOWN)

def get_all_blockout_settings():
    conn = sqlite3.connect(THP45_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM blockout_settings")
    rows = cursor.fetchall()
    conn.close()
    print("Blockout Settings:")
    for row in rows:
        print(row)
    return rows

if __name__ == "__main__":
    setup_gpio()
    simulate_setup_mode()
    enter_blockout_mode()
    short_press(BUTTON_GPIO_ENTER)
    GPIO.cleanup()
    get_all_blockout_settings()