import logging
from flask import Blueprint, jsonify

bp = Blueprint("machine", __name__)

def init_routes(state_machine):

    # ---------------- START ----------------
    @bp.route("/start", methods=["POST"])
    def start():
        logging.info("START cycle demandé")
        state_machine.start()
        return jsonify({"status": "started"})

    # ---------------- STOP ----------------
    @bp.route("/stop", methods=["POST"])
    def stop():
        logging.warning("STOP demandé")

        state_machine.stop()
        state_machine.worker.emergency_stop()

        return jsonify({"status": "stopped"})

    # ---------------- RESET ----------------
    @bp.route("/reset", methods=["POST"])
    def reset():
        logging.info("RESET machine")

        state_machine.reset()
        return jsonify({"status": "reset"})

    # ---------------- HOMING ----------------
    @bp.route("/home", methods=["POST"])
    def home():
        logging.info("HOMING demandé")

        try:
            state_machine.worker.home()
            return jsonify({"status": "homed"})
        except Exception as e:
            logging.error(str(e))
            return jsonify({"error": str(e)}), 500

    # ---------------- STATUS ----------------
    @bp.route("/status")
    def status():
        return jsonify(state_machine.status())

    return bp