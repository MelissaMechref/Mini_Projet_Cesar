# =============================================================================
# casser_enigma.py — Cassage automatique du chiffrement Enigma César
# =============================================================================
# Méthode : analyse de fréquences des lettres + score Chi-carré.
# Pour Enigma, on teste toutes les combinaisons (26³ = 17576) ou version optimisée
# qui exploite la structure cyclique (26×3 = 78 tests)
# =============================================================================

import enigma
import utile

# Fréquences des lettres en français (source: Beker & Piper)
FREQ = {
    'a': 0.0812, 'b': 0.0090, 'c': 0.0334, 'd': 0.0367, 'e': 0.1474, 'f': 0.0106,
    'g': 0.0084, 'h': 0.0073, 'i': 0.0757, 'j': 0.0061, 'k': 0.0001, 'l': 0.0545,
    'm': 0.0296, 'n': 0.0709, 'o': 0.0534, 'p': 0.0302, 'q': 0.0099, 'r': 0.0669,
    's': 0.0795, 't': 0.0724, 'u': 0.0637, 'v': 0.0164, 'w': 0.0001, 'x': 0.0038,
    'y': 0.0019, 'z': 0.0009,
}


def compter_frequences(texte):
    """
    Calcule la fréquence relative (0-1) de chaque lettre dans le texte.
    Ignore les caractères non alphabétiques.
    """
    compteurs = {l: 0 for l in utile.ALPHABET_MIN}
    total = 0
    for c in texte.lower():
        if utile.est_lettre(c):
            compteurs[c] += 1
            total += 1
    if total == 0:
        return compteurs
    # Division par le total pour obtenir des fréquences (somme = 1)
    return {l: compteurs[l] / total for l in utile.ALPHABET_MIN}


def score_chi_carre(freq_obs):
    """
    Calcule l'écart entre la distribution observée et celle du français.
    Plus le score est bas, plus le texte ressemble à du français.
    Formule: χ² = Σ (observé - attendu)² / attendu
    """
    return sum((freq_obs[l] - FREQ[l]) ** 2 / FREQ[l] for l in utile.ALPHABET_MIN if FREQ[l] > 0)
