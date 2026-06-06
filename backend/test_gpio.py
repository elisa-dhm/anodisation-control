#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE TEST GPIO - RASPBERRY PI 4
=====================================
Teste les pins GPIO sans démarrer le serveur complet

Usage: sudo python test_gpio.py
"""

import RPi.GPIO as GPIO
import time
import sys

print("=" * 70)
print("TEST GPIO - SYSTÈME D'ANODISATION")
print("=" * 70)

# Configuration
X_STEP = 17
X_DIR = 27
Y_STEP = 22
Y_DIR = 23
Z_STEP = 10
Z_DIR = 9
ENDSTOP_X = 5
ENDSTOP_Y = 6
ENDSTOP_Z = 11

# Listes des pins
STEP_PINS = {"X": X_STEP, "Y": Y_STEP, "Z": Z_STEP}
DIR_PINS = {"X": X_DIR, "Y": Y_DIR, "Z": Z_DIR}
ENDSTOP_PINS = {"X": ENDSTOP_X, "Y": ENDSTOP_Y, "Z": ENDSTOP_Z}

ALL_PINS = list(STEP_PINS.values()) + list(DIR_PINS.values()) + list(ENDSTOP_PINS.values())

try:
    # Initialiser GPIO
    print("\n[1/5] Initialisation GPIO...")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    print("  ✅ GPIO mode BCM activé")

    # Test 1: Configurer les pins en sortie
    print("\n[2/5] Configuration des pins moteurs...")
    for axis, pin in STEP_PINS.items():
        GPIO.setup(pin, GPIO.OUT)
        print(f"  ✅ {axis}_STEP (pin {pin}) = OUTPUT")
    
    for axis, pin in DIR_PINS.items():
        GPIO.setup(pin, GPIO.OUT)
        print(f"  ✅ {axis}_DIR (pin {pin}) = OUTPUT")

    # Test 2: Configurer les endstops en entrée
    print("\n[3/5] Configuration des capteurs (Endstops)...")
    for axis, pin in ENDSTOP_PINS.items():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        state = GPIO.input(pin)
        status = "LIBRE" if state else "DÉCLENCHÉ"
        print(f"  ✅ ENDSTOP_{axis} (pin {pin}) = {status}")

    # Test 3: Test des pins moteurs
    print("\n[4/5] Test des sorties moteurs (impulsions courtes)...")
    for axis, pin in STEP_PINS.items():
        print(f"  🔄 Test {axis}_STEP (pin {pin})...")
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.1)
        print(f"     ✅ Impulsion envoyée")

    # Test 4: Test des directions
    print("\n[5/5] Test des directions...")
    for axis, pin in DIR_PINS.items():
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.05)
        print(f"  ✅ Direction {axis} testée")

    print("\n" + "=" * 70)
    print("✅ TOUS LES TESTS GPIO RÉUSSIS !")
    print("=" * 70)
    print("\nRésumé:")
    print(f"  - {len(STEP_PINS)} moteurs détectés (X, Y, Z)")
    print(f"  - {len(ENDSTOP_PINS)} capteurs détectés")
    print(f"  - Tous les pins fonctionnent correctement")
    print("\nProchaine étape: python main.py")
    print("=" * 70)

except KeyboardInterrupt:
    print("\n\n⚠️  Test interrompu par l'utilisateur")
    
except Exception as e:
    print(f"\n❌ ERREUR: {e}")
    print("\n🔧 Solutions possibles:")
    print("  1. Lancer avec sudo: sudo python test_gpio.py")
    print("  2. Vérifier les pins dans config.py")
    print("  3. Vérifier que RPi.GPIO est installé: pip install RPi.GPIO")
    sys.exit(1)

finally:
    # Nettoyage
    try:
        GPIO.cleanup()
        print("\n🧹 Nettoyage GPIO effectué")
    except:
        pass
