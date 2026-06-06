#!/bin/bash
# ================================================
# SCRIPT TESTING RAPIDE - TEST COMPLET EN 5 MIN
# ================================================
# Usage: bash test_all.sh

set -e  # S'arrêter en cas d'erreur

RESET='\033[0m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'

echo -e "${BLUE}================================================${RESET}"
echo -e "${BLUE}TESTING COMPLET - SYSTÈME D'ANODISATION${RESET}"
echo -e "${BLUE}================================================${RESET}"

# Test 1: Vérifier qu'on est dans le bon dossier
echo -e "\n${YELLOW}[1/4] Vérification de l'environnement...${RESET}"
if [ ! -f "main.py" ]; then
    echo -e "${RED}❌ Erreur: main.py non trouvé${RESET}"
    echo -e "Lancer ce script depuis le dossier 'backend'"
    exit 1
fi
echo -e "${GREEN}✅ Dossier correct${RESET}"

# Test 2: Compatibilité
echo -e "\n${YELLOW}[2/4] Test de compatibilité...${RESET}"
if python test_compatibility.py > /tmp/test_compat.log 2>&1; then
    echo -e "${GREEN}✅ Tous les composants compatibles${RESET}"
else
    echo -e "${RED}❌ Erreur de compatibilité${RESET}"
    cat /tmp/test_compat.log
    exit 1
fi

# Test 3: GPIO (avec confirmation)
echo -e "\n${YELLOW}[3/4] Test GPIO...${RESET}"
echo -e "${YELLOW}⚠️  Ce test nécessite sudo et testera les pins GPIO${RESET}"
read -p "Continuer avec les tests GPIO? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if sudo python test_gpio.py > /tmp/test_gpio.log 2>&1; then
        echo -e "${GREEN}✅ GPIO fonctionnel${RESET}"
    else
        echo -e "${RED}❌ Erreur GPIO${RESET}"
        cat /tmp/test_gpio.log
    fi
else
    echo -e "${YELLOW}⏭️  GPIO skippé${RESET}"
fi

# Test 4: Serveur
echo -e "\n${YELLOW}[4/4] Test serveur (démarrage en arrière-plan)...${RESET}"
echo -e "${YELLOW}Lancement du serveur...${RESET}"
python main.py &
SERVER_PID=$!

# Attendre le démarrage
sleep 3

# Vérifier le serveur
if curl -s http://localhost:5000/api/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Serveur démarré avec succès${RESET}"
    echo -e "${GREEN}✅ API accessible à http://localhost:5000${RESET}"
    echo -e "${GREEN}✅ Frontend accessible à http://localhost:5000${RESET}"
    
    # Afficher les instructions finales
    echo -e "\n${BLUE}================================================${RESET}"
    echo -e "${GREEN}✅ TOUS LES TESTS RÉUSSIS !${RESET}"
    echo -e "${BLUE}================================================${RESET}"
    echo -e "\n${YELLOW}Prochaines étapes:${RESET}"
    echo -e "  1. Ouvrir navigateur: ${BLUE}http://localhost:5000${RESET}"
    echo -e "  2. Cliquer 'Homing'"
    echo -e "  3. Cliquer 'Démarrer'"
    echo -e "  4. Observer le cycle"
    echo -e "\n${YELLOW}Pour arrêter le serveur: Ctrl+C${RESET}"
    echo -e "${BLUE}================================================${RESET}\n"
    
    # Garder le serveur actif
    wait $SERVER_PID
else
    echo -e "${RED}❌ Serveur ne répond pas${RESET}"
    kill $SERVER_PID 2>/dev/null || true
    exit 1
fi
