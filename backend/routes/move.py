"""
Routes API pour le contrôle de la machine d'anodisation

Les routes sont enregistrées avec le préfixe /api/
"""

import logging
from flask import Blueprint, jsonify, request


bp = Blueprint("machine", __name__, url_prefix="/api")

logger = logging.getLogger(__name__)


def init_routes(sm):
    """
    Initialiser les routes de la machine
    
    Parameters:
    - sm: StateMachine instance
    """

    # ========================================
    # ROUTES DE CONTRÔLE
    # ========================================

    @bp.route("/start", methods=["POST"])
    def start():
        """Démarrer la machine d'anodisation"""
        try:
            if not sm.homed:
                return jsonify({
                    "status": "error",
                    "message": "Machine non homée. Effectuez le homing d'abord."
                }), 400
            
            logger.info("Démarrage de la machine...")
            sm.start()
            return jsonify({"status": "started"}), 200
        except Exception as e:
            logger.error(f"Erreur démarrage: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

    @bp.route("/stop", methods=["POST"])
    def stop():
        """Arrêter la machine d'anodisation"""
        try:
            logger.info("Arrêt de la machine...")
            sm.stop()
            return jsonify({"status": "stopped"}), 200
        except Exception as e:
            logger.error(f"Erreur arrêt: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

    @bp.route("/reset", methods=["POST"])
    def reset():
        """Réinitialiser la machine"""
        try:
            logger.info("Réinitialisation de la machine...")
            sm.reset()
            return jsonify({"status": "reset"}), 200
        except Exception as e:
            logger.error(f"Erreur réinitialisation: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

    @bp.route("/homing", methods=["POST"])
    def homing():
        """Effectuer le homing des moteurs"""
        try:
            logger.info("Début du homing...")
            sm.worker.home()
            sm.homed = True
            logger.info("Homing complété avec succès")
            return jsonify({
                "status": "homed",
                "position": {
                    "x": sm.worker.controller.current_x,
                    "y": sm.worker.controller.current_y,
                    "z": sm.worker.controller.current_z
                }
            }), 200
        except Exception as e:
            logger.error(f"Erreur homing: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

    @bp.route("/status", methods=["GET"])
    def get_status():
        """Obtenir l'état complet de la machine"""
        try:
            status = sm.status()
            from config import IMMERSION_TIME, STEP_DELAY_MIN, STEP_DELAY_MAX
            
            return jsonify({
                "homed": sm.homed,
                "running": status["running"],
                "position": {
                    "x": status["x"],
                    "y": status["y"],
                    "z": status["z"]
                },
                "current_bac": status["index"],
                "error": None,
                "config": {
                    "immersion_time": IMMERSION_TIME,
                    "step_delay_min": STEP_DELAY_MIN,
                    "step_delay_max": STEP_DELAY_MAX
                }
            }), 200
        except Exception as e:
            logger.error(f"Erreur statut: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

    @bp.route("/move", methods=["POST"])
    def manual_move():
        """Effectuer un mouvement manuel
        
        Body JSON attendu:
        {
            "x": 0,
            "y": 0,
            "z": 0
        }
        """
        try:
            data = request.get_json()
            x = data.get("x", sm.worker.controller.current_x)
            y = data.get("y", sm.worker.controller.current_y)
            z = data.get("z", sm.worker.controller.current_z)
            
            logger.info(f"Mouvement manuel vers ({x}, {y}, {z})")
            sm.worker.add_job(x, y, z)
            
            return jsonify({
                "status": "moving",
                "target": {"x": x, "y": y, "z": z}
            }), 200
        except Exception as e:
            logger.error(f"Erreur mouvement: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

    return bp
