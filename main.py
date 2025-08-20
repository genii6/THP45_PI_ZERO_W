import RPi.GPIO as GPIO
import time
import sqlite3
import sys

BUTTON_GPIO_UP = 22
BUTTON_GPIO_DOWN = 27
BUTTON_GPIO_ENTER = 17

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

def enter_setup_mode():
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
    short_press(BUTTON_GPIO_ENTER)

# Setup the blockout time here.
def set_blockout_time(setting):
    print(f"Setting blockout time for: {setting}")
    row = get_blockout_setting_by_name(setting)
    print(f"Blockout Setting: {row}")

def get_active_blockout_setting():
    conn = sqlite3.connect(THP45_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM blockout_settings WHERE active = 1")
    row = cursor.fetchone()
    conn.close()
    print(f"Active Blockout Setting: ['{row}']")
    return row[0][1] if row else None

def get_blockout_setting_by_name(setting_name):
    conn = sqlite3.connect(THP45_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM blockout_settings WHERE setting_name = ?", (setting_name,))
    row = cursor.fetchone()
    conn.close()
    return row if row else None

def is_valid_blockout_setting(setting):
    active_setting = get_active_blockout_setting()
    print("Active Blockout Setting:", active_setting)
    if active_setting == setting:
        print(f"Blockout setting ['{setting}'] is already active. Nothing to do...")
        return False
    return True

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(f"The script name is: {sys.argv[0]}")
        print(f"The first argument is: {sys.argv[1]}")
        if is_valid_blockout_setting(sys.argv[1]):
            setup_gpio()
            enter_setup_mode()
            enter_blockout_mode()
            set_blockout_time(sys.argv[1])
            GPIO.cleanup()
    else:
        print("Please specify only one argument. [disabled / peak / overnight]")