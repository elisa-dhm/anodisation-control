#!/bin/bash
# ================================================
# Script de Démarrage - Système d'Anodisation
# ================================================
# Usage: ./start.sh

echo "========================================"
echo "Démarrage du Système de Contrôle"
echo "========================================"

# Vérifier que nous sommes dans le bon dossier
if [ ! -f "main.py" ]; then
    echo "❌ Erreur: main.py non trouvé"
    echo "Lancer ce script depuis le dossier 'backend'"
    exit 1
fi

# Vérifier les permissions GPIO
if [ ! -w "/dev/gpiomem" ] && [ ! -w "/dev/mem" ]; then
    echo "⚠️  Attention: Permissions GPIO insuffisantes"
    echo "Les options:"
    echo "  1) Lancer avec sudo: sudo bash start.sh"
    echo "  2) Ajouter au groupe GPIO: sudo usermod -a -G gpio \$USER"
    echo ""
    read -p "Continuer quand même? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Lancer le serveur
echo "📍 Lancement du serveur..."
echo "   Adresse: http://0.0.0.0:5000"
echo ""
python main.py

# Cleanup
echo ""
echo "Arrêt du serveur"
