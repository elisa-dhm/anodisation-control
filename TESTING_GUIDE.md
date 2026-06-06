# 🧪 GUIDE DE TEST COMPLET - RASPBERRY PI 4

## 📋 Table des matières

1. [Pré-requis](#pré-requis)
2. [Test 1: Compatibilité](#test-1-compatibilité)
3. [Test 2: GPIO Matériel](#test-2-gpio-matériel)
4. [Test 3: API REST](#test-3-api-rest)
5. [Test 4: Frontend](#test-4-frontend)
6. [Test 5: Système Complet](#test-5-système-complet)
7. [Dépannage](#dépannage)

---

## ✅ Pré-requis

### Avoir sur le Raspberry Pi:

- ✅ Python 3.7+ (RPi a 3.9+ par défaut)
- ✅ pip installé : `sudo apt-get install python3-pip`
- ✅ Dépendances : `pip install -r requirements.txt`
- ✅ Fichiers du projet dans `/home/pi/anodisation/`

### Permissions GPIO

Pour éviter les erreurs de permissions, deux options:

**Option A: Lancer avec sudo (simple mais moins sûr)**
```bash
sudo python main.py
sudo python test_gpio.py
```

**Option B: Ajouter au groupe GPIO (recommandé)**
```bash
sudo usermod -a -G gpio $USER
# Puis redémarrer ou :
newgrp gpio
```

---

## 🧪 Test 1: Compatibilité

**Vérifier que tout est installé correctement**

```bash
cd ~/anodisation/backend
python test_compatibility.py
```

### Résultat attendu:

```
[1/6] Vérification Python...
  ✅ Python 3.9

[2/6] Vérification Flask...
  ✅ Flask 2.3.2

[3/6] Vérification Flask-CORS...
  ✅ Flask-CORS trouvé

[4/6] Vérification RPi.GPIO...
  ✅ RPi.GPIO trouvé
  ✅ Détecté: Raspberry Pi 4 Model B Rev 1.4

[5/6] Vérification structure...
  ✅ main.py
  ✅ config.py
  ...

[6/6] Vérification configuration...
  ✅ Configuration chargée

✅ TOUS LES TESTS PASSENT - SYSTÈME COMPATIBLE !
```

---

## 🔌 Test 2: GPIO Matériel

**Tester les pins GPIO physiques**

### IMPORTANT: Connecter les moteurs et endstops d'abord!

Vérifier le câblage selon `config.py`:
```
Moteurs STEP:    X=17, Y=22, Z=10
Moteurs DIR:     X=27, Y=23, Z=9
Endstops:        X=5, Y=6, Z=11
```

### Lancer le test GPIO:

```bash
# ATTENTION: Nécessite des droits root pour accéder aux GPIO
sudo python test_gpio.py
```

### Résultat attendu:

```
TEST GPIO - SYSTÈME D'ANODISATION

[1/5] Initialisation GPIO...
  ✅ GPIO mode BCM activé

[2/5] Configuration des pins moteurs...
  ✅ X_STEP (pin 17) = OUTPUT
  ✅ X_DIR (pin 27) = OUTPUT
  ...

[3/5] Configuration des capteurs (Endstops)...
  ✅ ENDSTOP_X (pin 5) = LIBRE
  ✅ ENDSTOP_Y (pin 6) = LIBRE
  ✅ ENDSTOP_Z (pin 11) = LIBRE

[4/5] Test des sorties moteurs...
  ✅ Impulsion envoyée (X)
  ✅ Impulsion envoyée (Y)
  ✅ Impulsion envoyée (Z)

[5/5] Test des directions...
  ✅ Direction X testée
  ✅ Direction Y testée
  ✅ Direction Z testée

✅ TOUS LES TESTS GPIO RÉUSSIS !
```

### Vérifications manuelles:

Pendant le test GPIO, vous devriez:
- 👂 Entendre les moteurs faire des clics (impulsions)
- 📊 Si vous appuyez sur les endstops, ils changent de "LIBRE" à "DÉCLENCHÉ"

---

## 🌐 Test 3: API REST

**Tester le serveur Flask et les endpoints**

### Terminal 1: Démarrer le serveur

```bash
cd ~/anodisation/backend
python main.py
```

Vous verrez:
```
========================================
Démarrage du système de contrôle
========================================
Serveur accessible à : http://0.0.0.0:5000
========================================
 * Running on http://127.0.0.1:5000
```

### Terminal 2: Lancer les tests API

```bash
cd ~/anodisation/backend
python test_api.py
```

### Résultat attendu:

```
TEST API REST - SYSTÈME D'ANODISATION

[1/8] Test health check...
  ✅ GET /api/health
     Réponse: {'status': 'OK', 'timestamp': '2026-05-31T...'}

[2/8] Récupération du statut...
  ✅ GET /api/status
     Homé: False
     Exécution: False
     Position: X=0, Y=0, Z=0

[3/8] Démarrage du homing...
  ✅ POST /api/homing
     {'status': 'homed', 'position': {...}}

[4/8] Vérification homing...
  ✅ Machine homée avec succès

[5/8] Test reset...
  ✅ POST /api/reset

[6/8] Test mouvement manuel...
  ✅ POST /api/move

[7/8] Test démarrage...
  ✅ POST /api/start

[8/8] Test arrêt...
  ✅ POST /api/stop

✅ TOUS LES TESTS API RÉUSSIS !
```

---

## 🎨 Test 4: Frontend

**Tester l'interface web**

### Depuis la RPi:

```bash
# Ouvrir le navigateur Chromium
chromium-browser http://localhost:5000
```

### Depuis un autre ordinateur:

```
http://<IP-RASPBERRY>:5000
```

**Trouver l'IP:**
```bash
hostname -I
# Résultat: 192.168.1.xxx
```

### Points à vérifier:

✅ **Page charge correctement**
- Logo visible
- Boutons colorés présents
- Pas de messages d'erreur

✅ **Informations en temps réel**
- Position X, Y, Z affichées
- État "Homé", "Exécution" mis à jour
- Badge de statut en haut

✅ **Boutons fonctionnent**
- Clicker "Homing" → Machine se calibre
- Clicker "Démarrer" → État change à "▶️ En cours"
- Clicker "Arrêter" → État change à "⏸️ Arrêtée"

✅ **Mouvement manuel**
- Entrer des valeurs XYZ
- Clicker "Déplacer" → Machine bouge

---

## 🤖 Test 5: Système Complet

**Test d'un cycle complet sans production**

### Étapes:

1. **Terminal 1: Démarrer le serveur**
   ```bash
   cd ~/anodisation/backend
   python main.py
   ```

2. **Terminal 2: Ouvrir navigateur**
   ```
   http://localhost:5000
   ```

3. **Vérifier le démarrage:**
   - ✅ Badge: "Initialisation..."
   - ✅ Position: X=0, Y=0, Z=0
   - ✅ État: Non homé

4. **Cliquer "🏠 Homing":**
   - ⏳ Attendre 5-10 secondes
   - ✅ Badge change à "Prêt"
   - ✅ Position: X=0, Y=0, Z=0 (référence)

5. **Cliquer "▶️ Démarrer":**
   - ⏳ Attendre 2-3 secondes
   - ✅ Badge change à "▶️ Exécution en cours"
   - ✅ Moteurs bougent (ou bruits si moteurs pas connectés)

6. **Vérifier les bains:**
   - ✅ Bain actuel change (1, 2, 3, 4, 1...)
   - ✅ Position change (X et Y changent)
   - ✅ Z descend après XY atteints
   - ✅ Temps d'immersion respecté

7. **Cliquer "⏹️ Arrêter":**
   - ✅ Mouvement s'arrête immédiatement
   - ✅ Badge change à "Prêt"

---

## 🐛 Dépannage

### Erreur: "Permission denied /dev/mem"

```bash
# Solution 1: Lancer avec sudo
sudo python main.py

# Solution 2: Ajouter au groupe GPIO
sudo usermod -a -G gpio $USER
newgrp gpio
python main.py
```

### Erreur: "ModuleNotFoundError: No module named 'flask'"

```bash
pip install Flask Flask-CORS
# Ou:
pip install -r requirements.txt
```

### Erreur: "ModuleNotFoundError: No module named 'RPi.GPIO'"

```bash
pip install RPi.GPIO
```

### Le serveur démarre mais le frontend ne s'affiche pas

1. Vérifier que `index.html` existe:
   ```bash
   ls ../frontend/index.html
   ```

2. Rafraîchir la page: `Ctrl+F5` ou `Cmd+Shift+R`

3. Vérifier les logs (erreurs en rouge dans le terminal)

### Les moteurs ne bougent pas

1. ✅ Vérifier l'alimentation
2. ✅ Tester GPIO manuellement: `sudo python test_gpio.py`
3. ✅ Vérifier les pins dans `config.py`
4. ✅ Vérifier les câbles

### Homing ne fonctionne pas

1. ✅ Vérifier que les endstops sont branchés
2. ✅ Tester manuellement:
   ```bash
   sudo python test_gpio.py
   # Appuyer sur les endstops et voir "LIBRE" → "DÉCLENCHÉ"
   ```
3. ✅ Vérifier les pins endstops dans `config.py`

### API retourne 500

Regarder les logs dans le terminal `main.py` pour voir l'erreur exacte.

Erreurs courantes:
- Moteurs pas branchés → Attendre timeout homing
- Pins GPIO incorrectes → Modifier `config.py`
- Permissions insuffisantes → Lancer avec `sudo`

### Frontend lent ou irresponsif

1. Vérifier CPU/Mémoire:
   ```bash
   top
   ```

2. Réduire la fréquence de mise à jour:
   - Ouvrir `frontend/index.html`
   - Ligne ~274: `const REFRESH_INTERVAL = 500` → 1000 (ms)

---

## 📊 Résumé des Tests

| Test | Commande | Durée | Résultat |
|------|----------|-------|----------|
| Compatibilité | `python test_compatibility.py` | 5s | ✅ Tous composants OK |
| GPIO | `sudo python test_gpio.py` | 10s | ✅ Pins fonctionnent |
| API | `python test_api.py` | 15s | ✅ Endpoints OK |
| Frontend | Browser: `http://localhost:5000` | - | ✅ Interface OK |
| Complet | Cycle bains + homing | 30s+ | ✅ Système OK |

---

## 🎯 Checklist Pré-Production

- [ ] `test_compatibility.py` ✅ réussit
- [ ] `test_gpio.py` ✅ réussit
- [ ] `test_api.py` ✅ réussit
- [ ] Frontend s'affiche correctement
- [ ] Homing fonctionne
- [ ] Moteurs bougent dans les 4 bains
- [ ] Arrêt d'urgence (bouton Stop) fonctionne
- [ ] Temps d'immersion respecté
- [ ] Z ne descend qu'après XY atteint
- [ ] API répond correctement à tous les endpoints

---

## 🚀 Passer à la Production

Une fois tous les tests réussis:

1. Définir les bains finaux dans `state_machine.py`
2. Ajuster les vitesses dans `config.py`
3. Tester les temps d'immersion réels
4. Vérifier les endstops physiquement
5. Lancer en boucle infinie: `python main.py`

Ou créer un service systemd pour démarrage automatique.

---

## 📞 Questions ?

- Consulter les logs: `python main.py 2>&1 | tee logs.txt`
- Vérifier les pins: `gpio readall` (si WiringPi installé)
- Tester GPIO: `sudo python test_gpio.py`

