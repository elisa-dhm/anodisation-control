import pigpio
import time


class StepperDriver:

    pi = None

    def __init__(self, step_pin, dir_pin, endstop_pin=None, invert_dir=False):

        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.endstop_pin = endstop_pin
        self.invert_dir = invert_dir

        self.endstop_available = False

        # Initialiser pigpio une seule fois
        if StepperDriver.pi is None:
            StepperDriver.pi = pigpio.pi()
            if not StepperDriver.pi.connected:
                raise RuntimeError("Impossible de se connecter à pigpiod. Assurez-vous que 'sudo systemctl start pigpiod' a été lancé.")

        # Configuration des pins
        StepperDriver.pi.set_mode(self.step_pin, pigpio.OUTPUT)
        StepperDriver.pi.set_mode(self.dir_pin, pigpio.OUTPUT)
        
        StepperDriver.pi.write(self.step_pin, 0)
        StepperDriver.pi.write(self.dir_pin, 0)

        if self.endstop_pin is not None:
            StepperDriver.pi.set_mode(self.endstop_pin, pigpio.INPUT)
            StepperDriver.pi.set_pull_up_down(self.endstop_pin, pigpio.PUD_UP)
            self.endstop_available = True

    def step(self, direction, pulse):

        # Inverser la direction si nécessaire
        if self.invert_dir:
            direction = not direction

        # Définir la direction
        StepperDriver.pi.write(self.dir_pin, 1 if direction else 0)
        
        # Très court délai pour la stabilisation
        time.sleep(0.00001)

        # Générer l'impulsion STEP
        # Utiliser une impulsion courte mais fiable
        pulse_duration = max(pulse, 0.00001)  # Minimum 10 microsecondes
        
        StepperDriver.pi.write(self.step_pin, 1)
        time.sleep(pulse_duration)
        StepperDriver.pi.write(self.step_pin, 0)
        time.sleep(pulse_duration)

    def read_endstop(self):

        if not self.endstop_available:
            return False

        return StepperDriver.pi.read(self.endstop_pin) == 0  # LOW quand pressé

    def read_endstop_filtered(self):

        if not self.endstop_available:
            return False

        hits = 0

        for _ in range(15):   # beaucoup plus léger
            if StepperDriver.pi.read(self.endstop_pin) == 0:
                hits += 1
            time.sleep(0.0001)

        return hits >= 3
