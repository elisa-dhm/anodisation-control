import RPi.GPIO as GPIO
import time
import logging
from config import STEP_DELAY_MIN

class StepperDriver:
    def __init__(self, step_pin, dir_pin):
        self.step_pin = step_pin
        self.dir_pin = dir_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(step_pin, GPIO.OUT)
        GPIO.setup(dir_pin, GPIO.OUT)

        logging.info(f"Driver STEP={step_pin} DIR={dir_pin}")

    def step(self, direction):
        GPIO.output(self.dir_pin, GPIO.HIGH if direction else GPIO.LOW)

        GPIO.output(self.step_pin, GPIO.HIGH)
        time.sleep(STEP_DELAY_MIN)
        GPIO.output(self.step_pin, GPIO.LOW)
