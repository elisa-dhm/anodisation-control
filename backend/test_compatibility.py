#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST DE COMPATIBILITÉ RASPBERRY PI 4
======================================
Script de vérification avant lancement de la machine

Usage: python test_compatibility.py
"""

import sys
import os

print("=" * 60)
print("TEST DE COMPATIBILITÉ - RASPBERRY PI 4")
print("=" * 60)

# ========================================
# Test 1: Version Python
# ========================================
print("\n[1/6] Vérification Python...")
try:
    if sys.version_info >= (3, 7):
        print(f"  ✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    else:
        print(f"  ❌ Python {sys.version_info.major}.{sys.version_info.minor} (minimum 3.7 requis)")
        sys.exit(1)
except Exception as e:
    print(f"  ❌ Erreur: {e}")
    sys.exit(1)

# ========================================
# Test 2: Flask
# ========================================
print("\n[2/6] Vérification Flask...")
try:
    import flask
    print(f"  ✅ Flask {flask.__version__}")
except ImportError:
    print("  ❌ Flask non installé")
    print("     Installer: pip install Flask==2.3.2")
    sys.exit(1)

# ========================================
# Test 3: Flask-CORS
# ========================================
print("\n[3/6] Vérification Flask-CORS...")
try:
    import flask_cors
    print(f"  ✅ Flask-CORS trouvé")
except ImportError:
    print("  ❌ Flask-CORS non installé")
    print("     Installer: pip install Flask-CORS==4.0.0")
    sys.exit(1)

# ========================================
# Test 4: RPi.GPIO
# ========================================
print("\n[4/6] Vérification RPi.GPIO...")
try:
    import RPi.GPIO
    print(f"  ✅ RPi.GPIO trouvé")
    
    # Vérifier que c'est un RPi
    try:
        with open('/proc/device-tree/model', 'r') as f:
            model = f.read().strip()
            if 'Raspberry Pi' in model:
                print(f"  ✅ Détecté: {model}")
            else:
                print(f"  ⚠️  Modèle: {model}")
    except:
        print("  ⚠️  Impossible de déterminer le modèle RPi")
        
except ImportError:
    print("  ❌ RPi.GPIO non installé")
    print("     Installer: pip install RPi.GPIO==0.7.0")
    print("     Note: Ce module ne fonctionne que sur Raspberry Pi")
    sys.exit(1)

# ========================================
# Test 5: Structure des fichiers
# ========================================
print("\n[5/6] Vérification structure des fichiers...")
try:
    required_files = [
        'main.py',
        'config.py',
        'motor/controller.py',
        'motor/driver.py',
        'motor/worker.py',
        'core/state_machine.py',
        'routes/move.py',
        '../frontend/index.html'
    ]
    
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    all_exist = True
    
    for file_path in required_files:
        full_path = os.path.join(backend_dir, file_path)
        if os.path.exists(full_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} NOT FOUND")
            all_exist = False
    
    if not all_exist:
        print("\n  Vérifier que vous êtes dans le dossier 'backend'")
        sys.exit(1)
        
except Exception as e:
    print(f"  ❌ Erreur: {e}")
    sys.exit(1)

# ========================================
# Test 6: Configuration
# ========================================
print("\n[6/6] Vérification configuration...")
try:
    # Importer sans inclure dans le path
    sys.path.insert(0, backend_dir)
    from config import (
        X_STEP, X_DIR, Y_STEP, Y_DIR, Z_STEP, Z_DIR,
        ENDSTOP_X, ENDSTOP_Y, ENDSTOP_Z,
        STEP_DELAY_MIN, STEP_DELAY_MAX, IMMERSION_TIME
    )
    
    print(f"  ✅ Configuration chargée")
    print(f"     - Moteur X: STEP={X_STEP} DIR={X_DIR}")
    print(f"     - Moteur Y: STEP={Y_STEP} DIR={Y_DIR}")
    print(f"     - Moteur Z: STEP={Z_STEP} DIR={Z_DIR}")
    print(f"     - Vitesse: MIN={STEP_DELAY_MIN}s MAX={STEP_DELAY_MAX}s")
    print(f"     - Immersion: {IMMERSION_TIME}s")
    
except Exception as e:
    print(f"  ❌ Erreur loading config: {e}")
    sys.exit(1)

# ========================================
# Résumé Final
# ========================================
print("\n" + "=" * 60)
print("✅ TOUS LES TESTS PASSENT - SYSTÈME COMPATIBLE !")
print("=" * 60)
print("\nVous pouvez maintenant lancer:")
print("  python main.py")
print("\nAccès au frontend:")
print("  http://localhost:5000")
print("=" * 60)
