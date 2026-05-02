# =========================
# GPIO
# =========================
X_STEP = 17
X_DIR  = 27

Y_STEP = 22
Y_DIR  = 23

ENABLE_PIN = 8   # 🔴 à ajouter si pas déjà

# =========================
# FIN DE COURSE
# =========================
ENDSTOP_X = 5
ENDSTOP_Y = 6

# =========================
# MOTEUR / CINÉMATIQUE
# =========================
MM_PER_STEP = 0.01   # 100 steps/mm

# =========================
# VITESSE
# =========================
STEP_DELAY_MIN = 0.00002   # rapide
STEP_DELAY_MAX = 0.0002    # lent (accélération)

# =========================
# HOMING
# =========================
HOMING_DELAY = 0.0001
HOMING_BACKOFF = 200
HOMING_TIMEOUT = 10  # secondes

# =========================
# SÉCURITÉ
# =========================
MAX_STEPS = 50000