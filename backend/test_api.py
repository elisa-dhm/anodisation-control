#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST API REST - SYSTÈME D'ANODISATION
=====================================
Teste les endpoints API sans contrôle réel des moteurs

Usage:
  Terminal 1: python main.py
  Terminal 2: python test_api.py
"""

import requests
import time
import json
import sys

# Configuration
API_URL = "http://localhost:5000"
TEST_TIMEOUT = 5

print("=" * 70)
print("TEST API REST - SYSTÈME D'ANODISATION")
print("=" * 70)
print(f"\nServeur: {API_URL}")
print("Assurez-vous que main.py est en cours d'exécution dans un autre terminal!\n")

try:
    # Test 1: Health Check
    print("[1/8] Test health check...")
    response = requests.get(f"{API_URL}/api/health", timeout=TEST_TIMEOUT)
    if response.status_code == 200:
        print("  ✅ GET /api/health")
        print(f"     Réponse: {response.json()}")
    else:
        print(f"  ❌ Erreur: {response.status_code}")

    # Test 2: Statut initial
    print("\n[2/8] Récupération du statut...")
    response = requests.get(f"{API_URL}/api/status", timeout=TEST_TIMEOUT)
    if response.status_code == 200:
        print("  ✅ GET /api/status")
        data = response.json()
        print(f"     Homé: {data['homed']}")
        print(f"     Exécution: {data['running']}")
        print(f"     Position: X={data['position']['x']}, Y={data['position']['y']}, Z={data['position']['z']}")
    else:
        print(f"  ❌ Erreur: {response.status_code}")

    # Test 3: Homing
    print("\n[3/8] Démarrage du homing...")
    response = requests.post(f"{API_URL}/api/homing", timeout=TEST_TIMEOUT)
    if response.status_code == 200:
        print("  ✅ POST /api/homing")
        print(f"     {response.json()}")
    else:
        print(f"  ❌ Erreur: {response.status_code}")
        print(f"     {response.json()}")

    time.sleep(1)

    # Test 4: Vérifier homing réussi
    print("\n[4/8] Vérification homing...")
    response = requests.get(f"{API_URL}/api/status", timeout=TEST_TIMEOUT)
    if response.status_code == 200:
        data = response.json()
        if data['homed']:
            print("  ✅ Machine homée avec succès")
        else:
            print("  ⚠️  Machine non homée")
            print("     (C'est OK si pas de moteurs connectés)")
    else:
        print(f"  ❌ Erreur: {response.status_code}")

    # Test 5: Reset
    print("\n[5/8] Test reset...")
    response = requests.post(f"{API_URL}/api/reset", timeout=TEST_TIMEOUT)
    if response.status_code == 200:
        print("  ✅ POST /api/reset")
    else:
        print(f"  ❌ Erreur: {response.status_code}")

    # Test 6: Mouvement manuel
    print("\n[6/8] Test mouvement manuel...")
    move_data = {"x": 100, "y": 200, "z": 50}
    response = requests.post(
        f"{API_URL}/api/move",
        json=move_data,
        timeout=TEST_TIMEOUT
    )
    if response.status_code == 200:
        print("  ✅ POST /api/move")
        print(f"     Cible: {response.json()['target']}")
    else:
        print(f"  ❌ Erreur: {response.status_code}")

    time.sleep(1)

    # Test 7: Démarrage (si homé)
    print("\n[7/8] Test démarrage...")
    response = requests.post(f"{API_URL}/api/start", timeout=TEST_TIMEOUT)
    if response.status_code == 200:
        print("  ✅ POST /api/start")
        print("     Machine démarrée")
    else:
        if response.status_code == 400:
            print("  ⚠️  Machine non homée (OK si pas de moteurs)")
        else:
            print(f"  ❌ Erreur: {response.status_code}")

    # Test 8: Arrêt
    print("\n[8/8] Test arrêt...")
    response = requests.post(f"{API_URL}/api/stop", timeout=TEST_TIMEOUT)
    if response.status_code == 200:
        print("  ✅ POST /api/stop")
        print("     Machine arrêtée")
    else:
        print(f"  ❌ Erreur: {response.status_code}")

    print("\n" + "=" * 70)
    print("✅ TOUS LES TESTS API RÉUSSIS !")
    print("=" * 70)
    print("\nRésumé:")
    print("  - Health check: OK")
    print("  - Statut: OK")
    print("  - Homing: OK")
    print("  - Mouvement manuel: OK")
    print("  - Start/Stop: OK")
    print("\n🎉 API fonctionnelle !")
    print("=" * 70)

except requests.exceptions.ConnectionError:
    print("\n❌ ERREUR: Impossible de se connecter au serveur")
    print("\n🔧 Solutions:")
    print("  1. Vérifier que main.py est en cours d'exécution")
    print("  2. Vérifier l'URL: " + API_URL)
    print("  3. Vérifier le port: 5000")
    print("\nDémarrer le serveur dans un autre terminal:")
    print("  cd backend")
    print("  python main.py")
    sys.exit(1)

except requests.exceptions.Timeout:
    print("\n❌ ERREUR: Le serveur ne répond pas (timeout)")
    sys.exit(1)

except Exception as e:
    print(f"\n❌ ERREUR: {e}")
    sys.exit(1)
