import threading
import time
import logging

from config import IMMERSION_TIME


class StateMachine:

    def __init__(self, worker):

        self.worker = worker

        self.state = "IDLE"
        self.running = False
        self.index = 0
        self.error = None
        self.homed = False

        self.bacs = [
            # ---- Bain 1 ----
            {"x": 45000, "y": 15000, "z": 3500, "immersion_time": 30},
            {"x": 45000, "y": 15000, "z": 0, "immersion_time": IMMERSION_TIME},
            # ---- Bain 2 ----
            {"x": 45000, "y": 63000, "z": 3500, "immersion_time": 30},
            {"x": 45000, "y": 63000, "z": 0, "immersion_time": IMMERSION_TIME},
            # ---- Bain 3 ----
            {"x": 45000, "y": 100000, "z": 3500, "immersion_time": 30},
            {"x": 45000, "y": 100000, "z": 0, "immersion_time": IMMERSION_TIME},
            # ---- Bain 4 ----
            {"x": 45000, "y": 63000, "z": 3500, "immersion_time": 30},
            {"x": 45000, "y": 63000, "z": 0, "immersion_time": IMMERSION_TIME},
            # ---- Bain 5 ----
            {"x": 3500, "y": 63000, "z": 3500, "immersion_time": 30},
            {"x": 3500, "y": 63000, "z": 0, "immersion_time": IMMERSION_TIME},
            # ---- Bain 6 ----
            {"x": 45000, "y": 63000, "z": 3500, "immersion_time": 30},
            {"x": 45000, "y": 63000, "z": 0, "immersion_time": IMMERSION_TIME},
            # ---- Bain 7 ----
            {"x": 3500, "y": 100000, "z": 3500, "immersion_time": 30},
            {"x": 3500, "y": 100000, "z": 0, "immersion_time": IMMERSION_TIME},
            # ---- Bain 8 ----
            {"x": 45000, "y": 63000, "z": 3500, "immersion_time": 30},
            {"x": 45000, "y": 63000, "z": 0, "immersion_time": IMMERSION_TIME},
            # ---- Position finale ----
            {"x": 3500, "y": 15000, "z": 3500, "immersion_time": 30},
            {"x": 3500, "y": 15000, "z": 0, "immersion_time": IMMERSION_TIME}
        ]

        threading.Thread(
            target=self.loop,
            daemon=True
        ).start()

    def loop(self):

        while True:

            if not self.running:
                time.sleep(0.1)
                continue

            bac = self.bacs[self.index]

            # Déplacement vers la position XYZ du bain
            self.worker.add_job(bac["x"], bac["y"], bac["z"])

            # Attendre que le mouvement soit terminé
            while not self.worker.queue.empty():
                time.sleep(0.05)

            # La pièce est maintenant immergée au bain
            immersion_time = bac.get("immersion_time", IMMERSION_TIME)
            logging.info(f"Bain {self.index}: immersion pendant {immersion_time}s à ({bac['x']}, {bac['y']}, {bac['z']})")
            
            # Attendre le temps d'immersion
            time.sleep(immersion_time)

            self.index = (self.index + 1) % len(self.bacs)

    def start(self):
        if not self.homed:
            return
        self.running = True

    def stop(self):
        self.running = False
        self.worker.emergency_stop()

    def reset(self):
        self.index = 0
        self.state = "IDLE"

    def status(self):
        return {
            "running": self.running,
            "index": self.index,
            "x": self.worker.controller.current_x,
            "y": self.worker.controller.current_y,
            "z": self.worker.controller.current_z
        }
