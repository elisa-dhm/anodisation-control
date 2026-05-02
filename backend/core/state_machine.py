import threading
import time
import logging

class StateMachine:
    def __init__(self, worker):

        self.worker = worker

        self.state = "IDLE"
        self.running = False
        self.index = 0
        self.error = None

        self.bacs = [
            {"x": 0, "y": 0, "time": 2},
            {"x": 10000, "y": 0, "time": 2},
            {"x": 10000, "y": 10000, "time": 2},
            {"x": 0, "y": 10000, "time": 2},
            {"x": 5000, "y": 5000, "time": 2},
        ]

        threading.Thread(target=self.loop, daemon=True).start()

    def loop(self):
        while True:

            if not self.running:
                time.sleep(0.1)
                continue

            try:
                self.state = "MOVE"

                bac = self.bacs[self.index]

                self.worker.controller.move_to(bac["x"], bac["y"])

                self.state = "ACTION"
                time.sleep(bac["time"])

                self.index += 1

                if self.index >= len(self.bacs):
                    self.index = 0

            except Exception as e:
                self.state = "ERROR"
                self.error = str(e)
                self.running = False

    def start(self):
        self.running = True
        self.state = "RUN"

    def stop(self):
        self.running = False
        self.state = "STOP"

    def reset(self):
        self.index = 0
        self.state = "IDLE"

    def status(self):
        return {
            "state": self.state,
            "index": self.index,
            "running": self.running,
            "error": self.error,
            "x": self.worker.controller.current_x,
            "y": self.worker.controller.current_y
        }
