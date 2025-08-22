import RPi.GPIO as GPIO
import time
import sqlite3
import sys
import datetime

BUTTON_GPIO_UP = 22
BUTTON_GPIO_DOWN = 27
BUTTON_GPIO_ENTER = 17

BUTTON_LONG_PRESS_DURATION = 3.0  # 3000ms
BUTTON_SHORT_PRESS_DURATION = 0.2  # 200ms
PAUSE_DURATION = 0.5  # 0.5 second

THP45_DB = '<HOME_DIR>/THP45_PI_ZERO_W/THP45.db'

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
    short_press(BUTTON_GPIO_UP)

# Setup the blockout time here.
def set_blockout_time(setting):
    print(f"Applying Blockout Setting: {setting}")
    row = get_blockout_setting_by_name(setting)
    print(f"Blockout Setting: {row}")
    if row:
        new_start_hour = row[2]
        new_end_hour = row[3]
        print(f"Setting Blockout Time: {new_start_hour} to {new_end_hour}")
        active_row = get_active_blockout_setting()
        active_start_hour = active_row[2]
        active_end_hour = active_row[3]
        print(f"Active Blockout Time: {active_start_hour} to {active_end_hour}")

        # Push the enter button to set the start hour
        short_press(BUTTON_GPIO_ENTER)

        # Calculate button pushes needed to set the new start hour
        pushes_to_start = calculate_button_pushes(active_start_hour, new_start_hour)
        for _ in range(pushes_to_start):
            short_press(BUTTON_GPIO_UP)

        # Push the enter button to set the end hour
        short_press(BUTTON_GPIO_ENTER)

        # Calculate button pushes needed to set the new end hour
        pushes_to_end = calculate_button_pushes(active_end_hour, new_end_hour)
        for _ in range(pushes_to_end):
            short_press(BUTTON_GPIO_UP)

        # Push the enter button to confirm the end hour
        short_press(BUTTON_GPIO_ENTER)
    else:
        print(f"No blockout setting found for: {setting}")

def get_active_blockout_setting():
    conn = sqlite3.connect(THP45_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM blockout_settings WHERE active = 1")
    row = cursor.fetchone()
    conn.close()
    print(f"Active Blockout Setting: ['{row}']")
    return row if row else None

def set_blockout_setting_active(setting_name):
    conn = sqlite3.connect(THP45_DB)
    cursor = conn.cursor()
    cursor.execute("UPDATE blockout_settings SET active = 0 WHERE active = 1")
    cursor.execute("UPDATE blockout_settings SET active = 1 WHERE setting_name = ?", (setting_name,))
    conn.commit()
    conn.close()
    print(f"Blockout setting '{setting_name}' is now active.")

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
    if active_setting[1] == setting:
        print(f"Blockout setting ['{setting}'] is already active. Nothing to do...")
        return False
    return True

def calculate_button_pushes(current_hour, new_hour):
    """
    Calculates the number of button pushes needed to go from current_hour to new_hour.
    Handles wrap-around for 24-hour format.
    """
    pushes = (new_hour - current_hour) % 24
    print(f"Button pushes needed to go from {current_hour} to {new_hour}: {pushes}")
    return pushes

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(f"Current Date/Time is: {datetime.datetime.now()}");
        print(f"Running Blockout Config script: {sys.argv[0]}")
        print(f"Provided Blockout Setting is: {sys.argv[1]}")
        if is_valid_blockout_setting(sys.argv[1]):
            setup_gpio()
            enter_setup_mode()
            enter_blockout_mode()
            set_blockout_time(sys.argv[1])
            set_blockout_setting_active(sys.argv[1])
            print("Blockout time set successfully.")
            GPIO.cleanup()
    else:
        print("Please specify only one argument. [disabled / peak / overnight]")