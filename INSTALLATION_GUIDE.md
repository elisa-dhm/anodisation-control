# 🏭 Système de Contrôle d'Anodisation - V2

Interface complète pour contrôler un système CNC d'anodisation avec 3 axes moteurs (X, Y, Z).

---

## 📋 Table des matières

1. [Installation](#installation)
2. [Démarrage](#démarrage)
3. [Paramètres Modifiables](#paramètres-modifiables)
4. [Architecture](#architecture)
5. [API Endpoints](#api-endpoints)

---

## 🚀 Installation

### Prérequis
- Python 3.7+
- Raspberry Pi avec GPIO

### Étapes

```bash
# 1. Naviguer au dossier backend
cd backend

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Démarrer le serveur
python main.py
```

Le serveur démarre sur `http://0.0.0.0:5000`

### Accès au Frontend

Ouvrir dans un navigateur : `http://<adresse-rpi>:5000`

---

## 📌 Paramètres Modifiables

### 🔧 Configuration Moteurs (`config.py`)

```python
# VITESSE DES MOTEURS
STEP_DELAY_MIN = 0.0025   # ⚡ Délai minimum = vitesse max
                          # Réduire pour aller plus vite
                          # Exemple: 0.002 pour accélérer

STEP_DELAY_MAX = 0.008    # Délai de démarrage (accélération)

# HOMING
HOMING_DELAY = 0.003      # Délai pendant le homing
HOMING_TIMEOUT = 10       # Timeout (secondes)

# IMMERSION
IMMERSION_TIME = 5        # ⏱️ Temps par défaut que la pièce reste immergée
                          # Modifiable par bain dans state_machine.py

# PINS GPIO
X_STEP = 17
X_DIR  = 27
Y_STEP = 22
Y_DIR  = 23
Z_STEP = 10
Z_DIR  = 9
ENABLE_PIN = 8

# ENDSTOPS (capteurs)
ENDSTOP_X = 5
ENDSTOP_Y = 6
ENDSTOP_Z = 11
```

### 🎮 Configuration Serveur (`main.py` ligne 170)

```python
app.run(
    host="0.0.0.0",        # 0.0.0.0 = accessible de partout
    port=5000,             # Port serveur
    debug=False,           # Mode debug
    threaded=False
)
```

### 🛁 Bains d'Anodisation (`state_machine.py`)

```python
self.bacs = [
    # Chaque bain avec ses coordonnées XYZ et temps d'immersion
    {"x": 0,     "y": 0,    "z": 0, "immersion_time": 5},     # Bain 1
    {"x": 5000,  "y": 0,    "z": 0, "immersion_time": 5},     # Bain 2
    {"x": 5000,  "y": 5000, "z": 0, "immersion_time": 10},    # Bain 3 (plus long)
    {"x": 0,     "y": 5000, "z": 0, "immersion_time": 5},     # Bain 4
]
```

### 🌐 Frontend (`frontend/index.html`)

```javascript
// Ligne 272
const API_URL = "http://localhost:5000";  // Adresse du serveur
const REFRESH_INTERVAL = 500;              // Fréquence mise à jour (ms)
```

---

## 🔄 Architecture du Système

```
┌─────────────────────────────────────┐
│        FRONTEND (HTML/JS)           │  Interface web moderne
└────────────────┬────────────────────┘
                 │ HTTP API (JSON)
                 ↓
┌─────────────────────────────────────┐
│      BACKEND (Flask)                │  main.py
│  - Gestion des routes API           │
│  - Orchestration des moteurs        │
└────────────────┬────────────────────┘
                 │
        ┌────────┴────────┬────────────┐
        ↓                 ↓            ↓
   ┌─────────┐      ┌─────────┐  ┌─────────┐
   │ Motor   │      │ State   │  │ Worker  │
   │Ctrl.   │      │Machine  │  │ Thread  │
   └────┬────┘      └────┬────┘  └────┬────┘
        │                │            │
        ↓                ↓            ↓
   ┌────────────────────────────────────┐
   │  Stepper Drivers (GPIO)            │
   │  - X, Y, Z Motors                  │
   │  - Endstop Sensors                 │
   └────────────────────────────────────┘
```

### Flux de Mouvement

1. **Commande** → Frontend envoie demande API
2. **Queue** → Worker reçoit et met en queue
3. **Mouvement XY** → X et Y se déplacent en parallèle
4. **Mouvement Z** → Z se déplace APRÈS atteinte XY
5. **Immersion** → Attente au bain
6. **Cycle** → Répétition

---

## 🔌 API Endpoints

### Santé du système

```
GET /api/health
Response: {"status": "OK", "timestamp": "2026-05-31T..."}
```

### Statut complet

```
GET /api/status
Response: {
  "homed": true,
  "running": false,
  "position": {"x": 0, "y": 0, "z": 0},
  "current_bac": 0,
  "error": null,
  "config": {
    "immersion_time": 5,
    "step_delay_min": 0.0025,
    "step_delay_max": 0.008
  }
}
```

### Homing

```
POST /api/homing
Response: {"status": "homed", "position": {...}}
```

### Démarrer

```
POST /api/start
Conditions: Machine doit être homée
Response: {"status": "started"}
```

### Arrêter

```
POST /api/stop
Response: {"status": "stopped"}
```

### Réinitialiser

```
POST /api/reset
Response: {"status": "reset"}
```

### Mouvement manuel

```
POST /api/move
Body: {"x": 1000, "y": 2000, "z": 500}
Response: {"status": "moving", "target": {...}}
```

---

## ⚙️ Astuces & Dépannage

### ⚡ Augmenter la vitesse

Réduire `STEP_DELAY_MIN` dans `config.py` (mais attention à la stabilité!)

```python
STEP_DELAY_MIN = 0.002  # Plus rapide
```

### 🔄 Inverser un moteur

Dans `controller.py`, fonction `move_to()`:

```python
# Ligne : self.x_motor.step(nx > px, delay)
# Changer à :
self.x_motor.step(nx < px, delay)  # Inverse X
```

### 📊 Activer les logs

```bash
# Dans le terminal, vous verrez les logs
# Pour sauvegarder dans fichier:
python main.py > logs.txt 2>&1
```

### 🐛 Debug

- Vérifier les pins GPIO dans `config.py`
- Vérifier les endstops : `GPIO.input(pin) == GPIO.LOW`
- Vérifier le connexion API : Console navigateur (F12)

---

## 📝 Notes d'Utilisation

- **Homing obligatoire** avant toute opération
- **Arrêt d'urgence** : Clic sur "Arrêter"
- **Mouvement Z sécurisé** : Z se déplace QUE après XY atteint
- **Temps d'immersion** : Configurable par bain

---

## 🎯 Workflow Typique

1. ✅ Démarrer le serveur : `python main.py`
2. ✅ Ouvrir frontend : `http://raspberry:5000`
3. ✅ Cliquer "Homing"
4. ✅ Cliquer "Démarrer"
5. 🔄 Système cycle automatiquement par les bains
6. ⏹️ Cliquer "Arrêter" pour interruption

---

## 📞 Support

Pour toute question, consultez les commentaires dans les fichiers:
- `main.py` - Endpoints et gestion
- `config.py` - Paramètres moteurs/GPIO
- `controller.py` - Logique de mouvement
- `state_machine.py` - Cycle de bains
- `frontend/index.html` - Configuration API (ligne 272)

