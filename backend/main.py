"""
===============================================
SYSTÈME DE CONTRÔLE D'ANODISATION
===============================================
Application Flask pour contrôler le système CNC d'anodisation

PARAMÈTRES MODIFIABLES :
- Port serveur : ligne 152 (port=5000)
- Adresse serveur : ligne 151 (host="0.0.0.0")
- Voir config.py pour les paramètres moteurs/timing
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import logging
import atexit
import pigpio
from datetime import datetime
import os

from motor.controller import CNCController
from motor.worker import MotorWorker
from core.state_machine import StateMachine
from routes.move import init_routes

# ============================================
# CONFIGURATION DU LOGGING
# ============================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================
# INITIALISATION FLASK ET COMPOSANTS
# ============================================
# Construire le chemin vers le dossier frontend de maniere robuste
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
CORS(app)  # Autoriser les requetes cross-origin pour le frontend

# Initialisation du contrôleur CNC
controller = CNCController()
worker = MotorWorker(controller)
sm = StateMachine(worker)

# Enregistrer les routes de mouvement avec le préfixe /api/
app.register_blueprint(init_routes(sm))

# ============================================
# ROUTES PRINCIPALES
# ============================================

@app.route("/", methods=["GET"])
def root():
    """Serve the frontend (index.html)"""
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/api/health", methods=["GET"])
def health_check():
    """Vérifier l'état de la machine"""
    return jsonify({
        "status": "OK",
        "timestamp": datetime.now().isoformat()
    }), 200


# ============================================
# GESTION DE L'ARRÊT PROPRE
# ============================================
def cleanup():
    """Nettoyer les ressources pigpio à l'arrêt"""
    logger.info("Nettoyage des ressources...")
    try:
        from motor.driver import StepperDriver
        if StepperDriver.pi is not None:
            StepperDriver.pi.stop()
    except Exception as e:
        logger.error(f"Erreur lors du nettoyage pigpio: {e}")


atexit.register(cleanup)

# ============================================
# POINT D'ENTRÉE
# ============================================
if __name__ == "__main__":
    logger.info("========================================")
    logger.info("Démarrage du système de contrôle")
    logger.info("========================================")
    logger.info(f"Serveur accessible à : http://0.0.0.0:5000")
    logger.info("========================================")
    
    # ⚙️ PARAMÈTRES MODIFIABLES :
    # Vous pouvez modifier ces paramètres selon vos besoins
    app.run(
        host="0.0.0.0",        # Adresse serveur (0.0.0.0 = accessible de partout)
        port=5000,             # Port serveur (modifiez pour utiliser un autre port)
        debug=False,           # Mode debug (False pour production)
        threaded=False         # Mode multithread
    )

