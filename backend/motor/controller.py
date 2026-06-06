import time
import logging

from motor.driver import StepperDriver
from config import *


class CNCController:

    def __init__(self):

        self.x_motor = StepperDriver(X_STEP, X_DIR, ENDSTOP_X, invert_dir=True)
        self.y_motor = StepperDriver(Y_STEP, Y_DIR, ENDSTOP_Y, invert_dir=True)
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

        # Étape 1 : Déplacer X et Y jusqu'à la position cible avec cinématique CoreXY
        dx = (tx - self.current_x)*-1
        dy = ty - self.current_y

        # Transformation CoreXY : conversion cartésien -> moteurs
        # motor1_steps = (dx + dy) / 2  (moteur X)
        # motor2_steps = (dx - dy) / 2  (moteur Y)
        motor1_steps = (dx + dy) / 2.0
        motor2_steps = (dx - dy) / 2.0

        steps_xy = int(max(abs(motor1_steps), abs(motor2_steps)))

        if steps_xy > 0:
            m1 = 0
            m2 = 0

            inc_m1 = motor1_steps / steps_xy
            inc_m2 = motor2_steps / steps_xy

            pm1 = m1
            pm2 = m2
            
            # Garder les positions initiales pour l'inverse transform
            base_x = self.current_x
            base_y = self.current_y

            delay = STEP_DELAY_MAX
            last_step_time = time.perf_counter()

            for step_count in range(steps_xy):

                if self.stop_flag:
                    logging.warning("STOP motion")
                    return

                # Attendre le délai exact sans time.sleep() imprécis
                while (time.perf_counter() - last_step_time) < delay:
                    pass  # Boucle serrée pour timing précis

                m1 += inc_m1
                m2 += inc_m2

                nm1 = round(m1)
                nm2 = round(m2)

                # Toujours appeler step pour chaque itération
                # Motor1 (X)
                if nm1 > pm1:
                    self.x_motor.step(True, 0)
                    pm1 = nm1
                elif nm1 < pm1:
                    self.x_motor.step(False, 0)
                    pm1 = nm1
                
                # Motor2 (Y)
                if nm2 > pm2:
                    self.y_motor.step(True, 0)
                    pm2 = nm2
                elif nm2 < pm2:
                    self.y_motor.step(False, 0)
                    pm2 = nm2

                # Mise à jour en temps réel avec inverse transform CoreXY
                self.current_x = base_x + nm1 + nm2
                self.current_y = base_y + nm1 - nm2

                last_step_time = time.perf_counter()

                # acceleration douce et progressive
                if delay > STEP_DELAY_MIN:
                    delay *= 0.85
                    if delay < STEP_DELAY_MIN:
                        delay = STEP_DELAY_MIN
        
        # S'assurer que les positions finales sont exactes
        self.current_x = tx
        self.current_y = ty

        # Étape 2 : Une fois X et Y atteints, bouger Z
        dz = (tz - self.current_z)*-1

        steps_z = int(abs(dz))

        if steps_z > 0:
            z = self.current_z

            inc_z = dz / steps_z

            pz = z

            delay = STEP_DELAY_MAX

            for _ in range(steps_z):

                if self.stop_flag:
                    logging.warning("STOP motion")
                    return

                z += inc_z

                nz = round(z)

                if nz != pz:
                    self.z_motor.step(nz > pz, delay)
                    pz = nz
                    self.current_z = nz

                # acceleration douce et progressive
                if delay > STEP_DELAY_MIN:
                    delay *= 0.95
                    if delay < STEP_DELAY_MIN:
                        delay = STEP_DELAY_MIN

    def home(self):

        start = time.time()

        hx = not self.x_motor.endstop_available
        hy = not self.y_motor.endstop_available
        hz = not self.z_motor.endstop_available
      
        while not (hx and hy and hz):

            if time.time() - start > HOMING_TIMEOUT:
                raise RuntimeError("Homing timeout")

            # =========================
            # 1) HOMING X
            # =========================
            if not hx:

                # mouvement X+ en CoreXY (A+ B+)
                self.x_motor.step(True, HOMING_DELAY)
                self.y_motor.step(True, HOMING_DELAY)

                if self.x_motor.read_endstop_filtered():
                    hx = True
                    self.current_x = 0

            # =========================
            # 2) HOMING Y
            # =========================
            if not hy:

                # mouvement Y+ en CoreXY (A- B+)
                self.x_motor.step(False, HOMING_DELAY)
                self.y_motor.step(True, HOMING_DELAY)

                if self.y_motor.read_endstop_filtered():
                    hy = True
                    self.current_y = 0

            # =========================
            # 3) Z indépendant
            # =========================
            if not hz:
                self.z_motor.step(False, HOMING_DELAY)
                if self.z_motor.read_endstop_filtered():
                    hz = True
                    self.current_z = 0

            time.sleep(HOMING_DELAY)
