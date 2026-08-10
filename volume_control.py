import RPi.GPIO as GPIO
import os
import time

# --- GPIO Pin Definitions ---
PIN_CLK = 18
PIN_DT = 17
PIN_SW = 27
volume_step = 5

# --- GPIO Initialization ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setwarnings(False)

# --- Full paths to commands ---
MPC_CMD = "/usr/bin/mpc -h localhost"
AMIXER_CMD = "/usr/bin/amixer"

# --- Callback Functions ---
def rotation_callback(channel):
    """Called when the CLK pin changes state"""
    time.sleep(0.002)  # Software debounce
    dt_state = GPIO.input(PIN_DT)

    if dt_state == GPIO.HIGH:
        os.system(f"{AMIXER_CMD} sset 'Master' {volume_step}%+") # Clockwise
    else:
        os.system(f"{AMIXER_CMD} sset 'Master' {volume_step}%-") # Counter-clockwise

def button_callback(channel):
    """Called when the button is pressed"""
    os.system(f"{MPC_CMD} toggle")

# --- Event Listeners (The Stable Method) ---
GPIO.add_event_detect(PIN_CLK, GPIO.FALLING, callback=rotation_callback, bouncetime=200)
GPIO.add_event_detect(PIN_SW, GPIO.FALLING, callback=button_callback, bouncetime=300)

print("Volume control service started successfully.")
try:
    while True:
        time.sleep(3600)
finally:
    GPIO.cleanup()
