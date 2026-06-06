from flask import Flask
import logging
import atexit
import RPi.GPIO as GPIO

from motor.controller import CNCController
from motor.worker import MotorWorker
from core.state_machine import StateMachine
from routes.move import init_routes


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

controller = CNCController()
worker = MotorWorker(controller)
sm = StateMachine(worker)

app.register_blueprint(init_routes(sm))


@app.route("/")
def ok():
    return "MACHINE OK"


def cleanup():
    GPIO.cleanup()


atexit.register(cleanup)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=False)