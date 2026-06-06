import logging
from flask import Blueprint, jsonify


bp = Blueprint("machine", __name__)


def init_routes(sm):

    @bp.route("/start", methods=["POST"])
    def start():
        sm.start()
        return jsonify({"status": "started"})

    @bp.route("/stop", methods=["POST"])
    def stop():
        sm.stop()
        return jsonify({"status": "stopped"})

    @bp.route("/reset", methods=["POST"])
    def reset():
        sm.reset()
        return jsonify({"status": "reset"})

    @bp.route("/home", methods=["POST"])
    def home():
        sm.worker.home()
        sm.homed = True
        return jsonify({"status": "homed"})

    @bp.route("/status")
    def status():
        return jsonify(sm.status())

    return bp