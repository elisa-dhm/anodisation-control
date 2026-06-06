import threading
import queue


class MotorWorker:

    def __init__(self, controller):

        self.controller = controller
        self.queue = queue.Queue()

        threading.Thread(
            target=self.run,
            daemon=True
        ).start()

    def add_job(self, x, y, z):
        self.queue.put((x, y, z))

    def emergency_stop(self):
        self.controller.emergency_stop()

        while not self.queue.empty():
            try:
                self.queue.get_nowait()
            except:
                break

    def home(self):
        self.controller.home()

    def run(self):

        while True:

            x, y, z = self.queue.get()

            try:
                self.controller.move_to(x, y, z)

            except Exception:
                pass

            self.queue.task_done()