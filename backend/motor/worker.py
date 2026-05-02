import threading
import queue
import logging

class MotorWorker:
    def __init__(self, controller):
        self.controller = controller
        self.queue = queue.Queue()

        threading.Thread(target=self.run, daemon=True).start()

    def add_job(self, x, y):
        self.queue.put((x, y))

    def run(self):
        while True:
            x, y = self.queue.get()
            try:
                self.controller.move_to(x, y)
            except Exception as e:
                logging.error(f"Motor error: {e}")
