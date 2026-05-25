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

def trouver_cle_enigma(texte):
    """
    Version force brute : teste TOUTES les 17576 combinaisons possibles.
    Garantie de trouver la bonne clé mais plus lente.
    """
    # Vérification : besoin d'au moins 20 lettres pour une analyse fiable
    nb = sum(1 for c in texte if utile.est_lettre(c))
    if nb < 20:
        print(f"AVERTISSEMENT: seulement {nb} lettre(s) (analyse peu fiable)")
        if nb == 0: return None, None

    print(f"Recherche parmi 26³=17576 combinaisons...")
    meilleure_cle, meilleur_score, meilleur_texte = None, float('inf'), ""

    # Trois boucles imbriquées pour tester toutes les clés de 0 à 25
    for k1 in range(26):
        for k2 in range(26):
            for k3 in range(26):
                # Déchiffrer avec la clé candidate
                dechiffre = enigma.enigma_dechiffrer(texte, (k1, k2, k3))
                # Calculer le score Chi-carré
                chi2 = score_chi_carre(compter_frequences(dechiffre))
                # Garder la meilleure clé (score le plus bas)
                if chi2 < meilleur_score:
                    meilleur_score, meilleure_cle, meilleur_texte = chi2, (k1, k2, k3), dechiffre

    print(f"\nClé trouvée: {meilleure_cle} (Score Chi²: {meilleur_score:.4f})")
    print(f"Message: {meilleur_texte}")
    return meilleure_cle, meilleur_texte


def trouver_cle_enigma_optimise(texte):
    """
    Version optimisée : exploite la structure cyclique d'Enigma.
    Les clés sont appliquées en boucle: position 0,1,2,0,1,2...
    On peut donc analyser SÉPARÉMENT chaque position de clé.

    Au lieu de 26³ tests, on fait 26 tests × 3 positions = 78 tests.
    Beaucoup plus rapide, mais suppose que le texte est assez long.
    """
    nb = sum(1 for c in texte if utile.est_lettre(c))
    if nb < 20:
        print(f"AVERTISSEMENT: seulement {nb} lettre(s)")
        if nb == 0: return None, None

    # Étape 1: séparer les lettres selon leur position modulo 3
    # Les lettres à la position 0 utilisent la clé1, position 1 → clé2, etc.
    lettres_pos = [[], [], []]
    pos = 0
    for c in texte:
        if utile.est_lettre(c):
            lettres_pos[pos].append(c)
            pos = (pos + 1) % 3  # Alterne 0,1,2,0,1,2...

    # Étape 2: pour chaque position, trouver la meilleure clé
    cle = []
    for i in range(3):
        meilleure_k, meilleur_score = 0, float('inf')
        # Tester les 26 clés possibles pour cette position
        for k in range(26):
            # Déchiffrer uniquement les lettres de cette position
            dechiffre = ''.join(
                utile.lettre_depuis_index((utile.index_lettre(c) - k) % 26, c)
                for c in lettres_pos[i]
            )
            chi2 = score_chi_carre(compter_frequences(dechiffre))
            if chi2 < meilleur_score:
                meilleur_score, meilleure_k = chi2, k
        cle.append(meilleure_k)

    # Étape 3: reconstituer la clé complète
    cle_finale = tuple(cle)
    texte_dechiffre = enigma.enigma_dechiffrer(texte, cle_finale)

    print(f"\nClé trouvée: {cle_finale}")
    print(f"Message: {texte_dechiffre}")
    return cle_finale, texte_dechiffre


def brute_force_enigma(texte, mode_optimise=True):
    """
    Interface principale.
    mode_optimise=True  → version rapide (78 tests) → recommandé
    mode_optimise=False → version exhaustive (17576 tests) → plus sûre
    """
    return trouver_cle_enigma_optimise(texte) if mode_optimise else trouver_cle_enigma(texte)
