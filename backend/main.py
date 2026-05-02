from flask import Flask, send_from_directory, jsonify
import logging
import os
import RPi.GPIO as GPIO
import atexit

from motor.controller import CNCController
from motor.worker import MotorWorker
from core.state_machine import StateMachine
from routes.move import init_routes

# ---------------- LOGS ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logging.info("Démarrage MACHINE ÉLOXAGE")

# ---------------- FRONTEND ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "../frontend"))

app = Flask(__name__, static_folder=FRONTEND_DIR)

# ---------------- MACHINE ----------------
controller = CNCController()
worker = MotorWorker(controller)
state_machine = StateMachine(worker)

# ---------------- ROUTES AUTO ----------------
app.register_blueprint(init_routes(state_machine))

# ---------------- FRONTEND ----------------
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

# ---------------- STATUS LIVE ----------------
@app.route("/status")
def status():
    return jsonify(state_machine.status())

# ---------------- TEST ----------------
@app.route("/test")
def test():
    return "OK MACHINE CONNECTED"

# ---------------- CLEANUP ----------------
def cleanup():
    try:
        GPIO.cleanup()
        logging.info("GPIO CLEANUP OK")
    except Exception as e:
        logging.error(f"GPIO cleanup error: {e}")

atexit.register(cleanup)

# ---------------- START ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
