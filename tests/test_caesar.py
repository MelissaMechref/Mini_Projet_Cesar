"""Tests pour le Mini-Projet A.

Ce fichier contient les chaînes de test officielles + quelques cas
limites. Ajoutez vos propres tests au fur et à mesure.

Pour lancer les tests :
    pip install pytest
    pytest -v
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import enigma
import casser_cesar
import casser_enigma

# Permet d'importer main.py depuis le dossier parent
from main import chiffrer, dechiffrer, enigma_chiffrer  # noqa: E402

# ---------- Chaînes de test officielles — César (spec §7) ----------

def test_cesar_officiel_cle_42():
    assert chiffrer("Veni, vidi, vici!", 42) == "Ludy, lyty, lysy!"


def test_cesar_officiel_cle_neg_42():
    assert chiffrer("Veni, vidi, vici!", -42) == "Foxs, fsns, fsms!"

# ---------- Chaîne de test officielle — Enigma César (spec §2.6) ----------

def test_enigma_officiel_maison():
    assert enigma_chiffrer("MAISON", (7, 16, 9)) == "TQRZEW"


# ---------- Cas standards (à compléter par votre équipe) ----------

def test_cesar_round_trip():
    """Chiffrer puis déchiffrer doit redonner le message original."""
    msg = "Bonjour le monde !"
    assert dechiffrer(chiffrer(msg, 7), 7) == msg

def test_enigma_round_trip():
    """Chiffrer puis déchiffrer avec Enigma doit redonner le message original."""
    msg = "Message de test enigma!"
    cle = (4, 12, 19)
    assert enigma.enigma_dechiffrer(enigma_chiffrer(msg, cle), cle) == msg
    
def test_cesar_cle_zero_identite():
    """Une clé de 0 ne doit rien changer."""
    assert chiffrer("Tout pareil.", 0) == "Tout pareil."
    
def test_cesar_chaine_vide():
    """Le chiffrement d'une chaîne vide doit retourner une chaîne vide."""
    assert chiffrer("", 15) == ""

def test_cesar_majuscules_minuscules():
    """Le chiffrement ne doit pas changer une lettre minuscule en majuscule et inversement."""
    assert chiffrer("AbCd", 1) == "BcDe"

def test_cesar_ponctuation_espaces():
    """Les caractères non alphabétiques doivent subir aucune modification."""
    assert chiffrer("Hello, World! 123", 5) == "Mjqqt, Btwqi! 123"
    
# TODO : ajoutez vos propres tests ci-dessous

def test_enigma_cles_negatives():
    """Enigma doit fonctionner correctement avec des clés négatives."""
    # Un décalage de -1 équivaut à un décalage de 25
    assert enigma_chiffrer("AAA", (-1, -2, -3)) == "ZYX"
    
def test_cesar_grandes_cles():
    """Le système modulo doit gérer les grandes clés sans erreur."""
    # Un décalage de 2600001 doit être équivalent à un décalage de 1.
    msg = "Test modulo grandes clés"
    assert chiffrer(msg, 2600001) == chiffrer(msg, 1)

def test_enigma_rejet_cle_invalide():
    """Une clé Enigma qui ne contient pas exactement 3 nombres doit être rejetée."""
    # pytest.raises vérifie que la fonction crash volontairement avec une ValueError
    with pytest.raises(ValueError):
        enigma_chiffrer("MAISON", (7, 16)) # Seulement 2 nombres
        
    with pytest.raises(ValueError):
        enigma_chiffrer("MAISON", (7, 16, 9, 2)) # 4 nombres

def test_bruteforce_cesar():
    """Vérifie que l'algorithme d'analyse fréquentielle retrouve la bonne clé César."""
    # Il faut que le texte soit assez long pour que l'analyse statistique fonctionne
    texte_clair = "Ceci est un message secret assez long pour lanalyse de frequence"
    texte_chiffre = chiffrer(texte_clair, 14)
    cle_trouvee, texte_trouve = casser_cesar.trouver_cle(texte_chiffre)
    assert cle_trouvee == 14

def test_bruteforce_enigma():
    """Vérifie que l'algorithme retrouve le bon triplet Enigma."""
    texte_clair = "Ceci est un message secret assez long pour lanalyse de frequence"
    cle_originale = (3, 14, 5)
    texte_chiffre = enigma_chiffrer(texte_clair, cle_originale)
    cle_trouvee, texte_trouve = casser_enigma.brute_force_enigma(texte_chiffre, mode_optimise=True)
    assert cle_trouvee == cle_originale
