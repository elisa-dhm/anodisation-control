import RPi.GPIO as GPIO
import time


class StepperDriver:

    gpio_ready = False

    def __init__(self, step_pin, dir_pin, endstop_pin=None):

        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.endstop_pin = endstop_pin

        self.endstop_available = False

        if not StepperDriver.gpio_ready:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            StepperDriver.gpio_ready = True

        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)

        GPIO.output(self.step_pin, GPIO.LOW)
        GPIO.output(self.dir_pin, GPIO.LOW)

        if self.endstop_pin is not None:

            GPIO.setup(self.endstop_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.endstop_available = True

    def step(self, direction, pulse):

        GPIO.output(
            self.dir_pin,
            GPIO.HIGH if direction else GPIO.LOW
        )

        time.sleep(0.001)

        pulse = max(pulse, 0.0025)

        GPIO.output(self.step_pin, GPIO.HIGH)
        time.sleep(pulse)

        GPIO.output(self.step_pin, GPIO.LOW)
        time.sleep(pulse)

    def read_endstop(self):

        if not self.endstop_available:
            return False

        return GPIO.input(self.endstop_pin) == GPIO.LOW