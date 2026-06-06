import time
import logging

from motor.driver import StepperDriver
from config import *


class CNCController:

    def __init__(self):

        self.x_motor = StepperDriver(X_STEP, X_DIR, ENDSTOP_X)
        self.y_motor = StepperDriver(Y_STEP, Y_DIR, ENDSTOP_Y)
        self.z_motor = StepperDriver(Z_STEP, Z_DIR, ENDSTOP_Z)

        self.current_x = 0
        self.current_y = 0
        self.current_z = 0

        self.stop_flag = False

    def emergency_stop(self):
        self.stop_flag = True

    def reset_stop(self):
        self.stop_flag = False

    def move_to(self, tx, ty, tz):

        self.stop_flag = False

        dx = tx - self.current_x
        dy = ty - self.current_y
        dz = tz - self.current_z

        steps = int(max(abs(dx), abs(dy), abs(dz)))

        if steps == 0:
            return

        x = self.current_x
        y = self.current_y
        z = self.current_z

        inc_x = dx / steps
        inc_y = dy / steps
        inc_z = dz / steps

        px = x
        py = y
        pz = z

        delay = STEP_DELAY_MAX

        for _ in range(steps):

            if self.stop_flag:
                logging.warning("STOP motion")
                return

            x += inc_x
            y += inc_y
            z += inc_z

            nx = round(x)
            ny = round(y)
            nz = round(z)

            if nx != px:
                self.x_motor.step(nx > px, delay)
                px = nx
                self.current_x = nx

            if ny != py:
                self.y_motor.step(ny > py, delay)
                py = ny
                self.current_y = ny

            if nz != pz:
                self.z_motor.step(nz > pz, delay)
                pz = nz
                self.current_z = nz

            # acceleration simple
            if delay > STEP_DELAY_MIN:
                delay *= 0.98
                if delay < STEP_DELAY_MIN:
                    delay = STEP_DELAY_MIN

    def home(self):
        # Simulation du homing sans fin de course
        # La position actuelle devient l'origine (0, 0, 0)
        self.current_x = 0
        self.current_y = 0
        self.current_z = 0