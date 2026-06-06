import threading
import time


class StateMachine:

    def __init__(self, worker):

        self.worker = worker

        self.state = "IDLE"
        self.running = False
        self.index = 0
        self.error = None
        self.homed = False

        self.bacs = [
            {"x": 0, "y": 0, "z": 0, "time": 1},
            {"x": 5000, "y": 0, "z": 0, "time": 1},
            {"x": 5000, "y": 5000, "z": 0, "time": 1},
            {"x": 0, "y": 5000, "z": 0, "time": 1},
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

            self.worker.add_job(bac["x"], bac["y"], bac["z"])

            # attente simple
            while not self.worker.queue.empty():
                time.sleep(0.05)

            time.sleep(bac["time"])

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