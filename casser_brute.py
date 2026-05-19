# =============================================================================
# casser_brute.py — Cassage automatique du chiffrement de César
# =============================================================================
# Méthode : analyse de fréquences des lettres + score Chi-carré.
# Aucune interaction utilisateur. Retourne directement la clé et le texte.
#
# Principe :
#   En français, la lettre 'e' est la plus fréquente (~14,7%), suivie de
#   's', 'a', 'n', 't', 'i', 'r', etc. Le chiffrement de César décale
#   toutes les lettres d'une valeur fixe, donc la lettre la plus fréquente
#   dans le texte chiffré correspond très probablement au 'e' original.
#
#   Pour chacune des 26 clés candidates, on déchiffre le texte et on mesure
#   l'écart entre la distribution des lettres obtenue et celle du français
#   via le score Chi-carré. La clé qui minimise cet écart est retenue.
# =============================================================================

import cesar
import utile


# -----------------------------------------------------------------------------
# FRÉQUENCES DE RÉFÉRENCE DU FRANÇAIS (source : Beker & Piper)
# Probabilité d'apparition de chaque lettre dans un texte français typique
# -----------------------------------------------------------------------------
FREQUENCES_FRANCAIS = {
    'a': 0.0812, 'b': 0.0090, 'c': 0.0334, 'd': 0.0367, 'e': 0.1474,
    'f': 0.0106, 'g': 0.0084, 'h': 0.0073, 'i': 0.0757, 'j': 0.0061,
    'k': 0.0001, 'l': 0.0545, 'm': 0.0296, 'n': 0.0709, 'o': 0.0534,
    'p': 0.0302, 'q': 0.0099, 'r': 0.0669, 's': 0.0795, 't': 0.0724,
    'u': 0.0637, 'v': 0.0164, 'w': 0.0001, 'x': 0.0038, 'y': 0.0019,
    'z': 0.0009,
}


def compter_frequences(texte):
    """
    Calcule la fréquence relative de chaque lettre dans un texte.
    Les caractères non alphabétiques sont ignorés.

    Paramètre :
        texte (str) : le texte à analyser

    Retourne :
        dict[str, float] : fréquences relatives pour 'a'..'z'
    """
    compteurs = {lettre: 0 for lettre in utile.ALPHABET_MIN}
    total = 0

    for c in texte.lower():
        if utile.est_lettre(c):
            compteurs[c] += 1
            total += 1

    if total == 0:
        return compteurs

    return {lettre: count / total for lettre, count in compteurs.items()}


def score_chi_carre(frequences_observees):
    """
    Mesure l'écart entre une distribution de lettres observée et celle
    du français de référence via le score Chi-carré.

    Un score faible → distribution proche du français → texte probablement déchiffré.
    Un score élevé → distribution chaotique → mauvaise clé.

    Formule : χ² = Σ (observé - attendu)² / attendu

    Paramètre :
        frequences_observees (dict[str, float]) : fréquences du texte candidat

    Retourne :
        float : score Chi-carré (plus bas = meilleur)
    """
    return sum(
        (frequences_observees[l] - FREQUENCES_FRANCAIS[l]) ** 2 / FREQUENCES_FRANCAIS[l]
        for l in utile.ALPHABET_MIN
    )


def trouver_cle(texte):
    """
    Trouve automatiquement la clé de César d'un texte chiffré
    par analyse de fréquences des lettres.

    Teste les 26 clés possibles, déchiffre le texte pour chacune,
    puis retient celle dont la distribution de lettres est la plus
    proche du français (score Chi-carré minimal).

    Paramètre :
        texte (str) : le texte chiffré

    Retourne :
        tuple (int, str) : (clé trouvée, texte déchiffré)
        ou (None, None) si le texte ne contient pas assez de lettres
    """
    nb_lettres = sum(1 for c in texte if utile.est_lettre(c))
    if nb_lettres < 20:
        print(f"AVERTISSEMENT : seulement {nb_lettres} lettre(s) détectée(s).")
        print("L'analyse de fréquences est peu fiable en dessous de 20 lettres.")
        if nb_lettres == 0:
            return None, None

    meilleure_cle = None
    meilleur_score = float('inf')
    meilleur_texte = ""

    for cle in range(26):
        texte_dechiffre = cesar.cesar_dechiffrer(texte, cle)
        freq = compter_frequences(texte_dechiffre)
        chi2 = score_chi_carre(freq)

        if chi2 < meilleur_score:
            meilleur_score = chi2
            meilleure_cle = cle
            meilleur_texte = texte_dechiffre

    print("=== Résultat brute-force ===")
    print(f"Clé trouvée    : {meilleure_cle}")
    print(f"Score Chi²     : {meilleur_score:.4f}  (plus bas = plus proche du français)")
    print("Message déchiffré :")
    print(meilleur_texte)

    return meilleure_cle, meilleur_texte


# Alias pour compatibilité avec main.py
def brute_force_auto(texte):
    return trouver_cle(texte)

