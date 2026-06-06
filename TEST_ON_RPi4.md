# 🧪 TEST SUR RASPBERRY PI 4 - DÉMARRAGE RAPIDE

## 📍 Où êtes-vous maintenant?

Vous avez le code qui est **✅ prêt et fonctionnel** pour RPi 4.

Maintenant, vous devez le **copier sur votre RPi** et le **tester étape par étape**.

---

## 🚀 Étape 1: Copier les fichiers sur la RPi

### Option A: Via SCP (depuis votre PC)

```bash
# Copier tout le projet
scp -r /chemin/vers/anodisation-control_V2 pi@192.168.1.xxx:/home/pi/

# Remplacer 192.168.1.xxx par l'IP de votre RPi
```

### Option B: Via Git

```bash
# Sur la RPi
cd ~
git clone <votre-repo>
cd anodisation-control_V2/backend
```

### Option C: Clé USB

1. Copier le dossier sur clé USB depuis Windows
2. Brancher la clé sur la RPi
3. Monter et copier

---

## 🔧 Étape 2: Installation des dépendances

### Sur la RPi, ouvrir un terminal et exécuter:

```bash
# Naviguer au dossier
cd ~/anodisation-control_V2/backend

# Installer les dépendances
pip install -r requirements.txt
```

**Temps:** ~5 minutes selon la connexion internet

**Résultat attendu:**
```
Successfully installed Flask-2.3.2 Flask-CORS-4.0.0 RPi.GPIO-0.7.0 ...
```

---

## ✅ Étape 3: Test de Compatibilité (5 secondes)

```bash
python test_compatibility.py
```

### Résultat attendu:

```
✅ Python 3.9
✅ Flask 2.3.2
✅ Flask-CORS
✅ RPi.GPIO
✅ Raspberry Pi 4 Model B
✅ Tous les fichiers présents
✅ Configuration OK

✅ TOUS LES TESTS PASSENT !
```

Si ❌ erreur → Voir la section "Dépannage" plus bas

---

## 🔌 Étape 4: Test GPIO (2 minutes) - OPTIONNEL

### IMPORTANT: Brancher les moteurs d'abord!

```bash
# Tester les pins GPIO
sudo python test_gpio.py
```

### Pendant le test:

- 👂 Vous entendez des clics (impulsions aux moteurs)
- 📊 Les endstops affichent "LIBRE" ou "DÉCLENCHÉ"

### Résultat attendu:

```
✅ GPIO mode BCM activé
✅ X_STEP (pin 17) = OUTPUT
✅ X_DIR (pin 27) = OUTPUT
...
✅ ENDSTOP_X (pin 5) = LIBRE
✅ ENDSTOP_Y (pin 6) = LIBRE
✅ ENDSTOP_Z (pin 11) = LIBRE

✅ Impulsions envoyées aux moteurs
✅ Directions testées

✅ TOUS LES TESTS GPIO RÉUSSIS !
```

---

## 🌐 Étape 5: Démarrage du Serveur

### Terminal 1: Démarrer le serveur

```bash
python main.py
```

### Résultat attendu:

```
========================================
Démarrage du système de contrôle
========================================
Serveur accessible à : http://0.0.0.0:5000
========================================
 * Running on http://127.0.0.1:5000
```

✅ **LE SERVEUR EST EN COURS D'EXÉCUTION**

Ne fermez pas ce terminal! Continuez dans un autre.

---

## 🌐 Étape 6: Test API (optional)

### Terminal 2 (nouveau): Tester les endpoints

```bash
python test_api.py
```

### Résultat attendu:

```
[1/8] Test health check...
  ✅ GET /api/health

[2/8] Récupération du statut...
  ✅ GET /api/status

[3/8] Démarrage du homing...
  ✅ POST /api/homing

...

✅ TOUS LES TESTS API RÉUSSIS !
```

---

## 🎨 Étape 7: Ouvrir le Frontend

### Depuis la RPi:

```bash
# Ouvrir Chromium
chromium-browser http://localhost:5000
```

### Depuis un autre PC:

```
Navigateur → http://<IP-RASPBERRY>:5000
```

**Trouver l'IP:**
```bash
hostname -I
```

### Vous devez voir:

```
┌─────────────────────────────────────────┐
│  🏭 Système de Contrôle d'Anodisation  │
│  Interface de gestion des moteurs CNC   │
│  ⚙️ ⚙️ ⚙️                              │
└─────────────────────────────────────────┘

[⚙️ Contrôle Principal]  [📍 Position]  [ℹ️ État]
[🎮 Mouvement Manuel]
```

---

## ✅ Étape 8: Test Complet du Système

### Cliquer sur les boutons dans cet ordre:

1. **🏠 Homing**
   - ⏳ Attendre 5-10 secondes
   - ✅ Badge passe à "Prêt" (vert)
   - 👂 Entendre les moteurs bouger

2. **▶️ Démarrer**
   - ✅ Badge passe à "▶️ Exécution en cours" (bleu)
   - 👂 Moteurs bougent
   - 📊 Bain actuel change: 1 → 2 → 3 → 4 → 1 ...
   - 📍 Position X, Y changent
   - ⏱️ Temps d'immersion respecté

3. **⏹️ Arrêter**
   - ✅ Moteurs s'arrêtent
   - ✅ Badge revient à "Prêt"

### Résultat final:

**✅ LE SYSTÈME FONCTIONNE CORRECTEMENT !**

---

## 🎯 Points Clés à Vérifier

### Hardware

- [ ] Moteurs pas-à-pas connectés
- [ ] Capteurs endstops connectés
- [ ] Alimentation OK
- [ ] Câbles serrés

### Software

- [ ] Dépendances installées
- [ ] Tests de compatibilité réussis
- [ ] Serveur démarre sans erreur
- [ ] Frontend s'affiche

### Fonctionnel

- [ ] Homing calibre les axes
- [ ] Moteurs bougent dans les 4 bains
- [ ] Z descend après XY
- [ ] Temps d'immersion respecté
- [ ] Arrêt d'urgence fonctionne

---

## 🧪 Test Rapide (All-in-One) - 5 MINUTES

```bash
# Si vous voulez tester tout d'un coup:
bash test_all.sh
```

Cela va:
1. ✅ Vérifier la compatibilité
2. ✅ Tester GPIO
3. ✅ Démarrer le serveur
4. ✅ Vous dire comment accéder au frontend

---

## 🐛 Dépannage Courant

### ❌ "Permission denied /dev/mem"

```bash
sudo python test_gpio.py
# Ou:
sudo python main.py
```

### ❌ "ModuleNotFoundError: No module named 'RPi.GPIO'"

```bash
pip install RPi.GPIO
```

### ❌ "Cannot connect to server"

- Vérifier que `python main.py` est en cours d'exécution
- Vérifier l'URL: `http://localhost:5000`
- Vérifier le port: `5000`

### ❌ Moteurs ne bougent pas

1. Vérifier l'alimentation: Multimètre sur les pins
2. Tester GPIO: `sudo python test_gpio.py`
3. Vérifier les pins dans `config.py`

### ❌ Frontend blanc/vide

- Rafraîchir la page: `Ctrl+F5`
- Vérifier les logs du serveur pour les erreurs (terminal)
- Vérifier que `index.html` existe: `ls ../frontend/index.html`

---

## 📊 Résumé des Tests

```
ÉTAPE                  COMMANDE                  DURÉE    RÉSULTAT
────────────────────────────────────────────────────────────────
1. Compatibilité       python test_compatibility.py  5s    ✅
2. GPIO                sudo python test_gpio.py      10s   ✅
3. Serveur + Frontend  python main.py                ∞     ✅
4. API                 python test_api.py            15s   ✅
5. Système Complet     Manuel via Frontend           30s   ✅
────────────────────────────────────────────────────────────────
                       TOTAL                         ~1min ✅
```

---

## 🎬 Vidéo Test (Résumé Visuel)

### Voici ce que vous verrez:

1. **Au démarrage:** Badge "Initialisation..." (gris)
2. **Après Homing:** Badge "Prêt" (vert) + Position = 0,0,0
3. **Au démarrage:** Badge "▶️ Exécution" (bleu) + Moteurs bougent
4. **Pendant le cycle:**
   - Bain 1: X=0, Y=0, puis Z baisse → attente 5s
   - Bain 2: X=5000, Y=0, puis Z baisse → attente 5s
   - Bain 3: X=5000, Y=5000, puis Z baisse → attente 10s
   - Bain 4: X=0, Y=5000, puis Z baisse → attente 5s
   - Cycle recommence...
5. **À l'arrêt:** Badge "Prêt" (vert), moteurs s'arrêtent

---

## 🏁 Objectif Final

Une fois tous ces tests réussis, vous avez un **système d'anodisation entièrement fonctionnel** !

### Configuration pour Production:

1. Adapter les coordonnées des bains dans `state_machine.py`
2. Ajuster les vitesses dans `config.py`
3. Tester les temps réels
4. Lancer `python main.py` en permanence

---

## 🚀 Besoin d'aide?

1. Consulter **TESTING_GUIDE.md** pour plus de détails
2. Consulter **RPi4_COMPATIBILITY_CHECK.md** pour le technique
3. Vérifier les logs: Regarder le terminal `main.py` pour les erreurs

**Bon testing! 🎉**

