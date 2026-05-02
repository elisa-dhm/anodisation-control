import logging
import time
from motor.driver import StepperDriver
from config import X_STEP, X_DIR, Y_STEP, Y_DIR, STEP_DELAY_MIN

class CNCController:
    def __init__(self):
        self.x_motor = StepperDriver(X_STEP, X_DIR)
        self.y_motor = StepperDriver(Y_STEP, Y_DIR)

        self.current_x = 0
        self.current_y = 0

        logging.info("Controller initialisé")

    def move_to(self, target_x, target_y):

        logging.info(f"Move_to → X={target_x} Y={target_y}")

        dx = target_x - self.current_x
        dy = target_y - self.current_y

        steps = int(max(abs(dx), abs(dy)))

        if steps == 0:
            return

        step_x = dx / steps
        step_y = dy / steps

        for _ in range(steps):

            self.current_x = int(self.current_x + step_x)
            self.current_y = int(self.current_y + step_y)

            # simulation step moteur
            if step_x != 0:
                self.x_motor.step(1 if step_x > 0 else 0)

            if step_y != 0:
                self.y_motor.step(1 if step_y > 0 else 0)

            time.sleep(STEP_DELAY_MIN)
