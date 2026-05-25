# =============================================================================
# casser_enigma_naive.py — Cassage naïf du chiffrement Enigma César
# =============================================================================
# Méthode : déchiffrage exhaustif des 26³ = 17 576 combinaisons + dictionnaire.
#
# Principe :
#   Pour chaque triplet (k1, k2, k3), on déchiffre le texte entier,
#   puis on compte combien de mots d'un dictionnaire français courant
#   apparaissent dans le résultat. Le triplet qui maximise ce score est retenu.
#
#   Aucune statistique, aucune fréquence — juste du texte et des mots.
#   ⚠ 17 576 déchiffrages complets : très lent sur les longs textes.
# =============================================================================

import timeit
import enigma
import utile


# Dictionnaire de mots français courants
MOTS_FRANCAIS = {
    "le", "la", "les", "de", "du", "des", "un", "une",
    "et", "en", "au", "aux", "ce", "se", "sa", "son",
    "est", "que", "qui", "ne", "pas", "sur", "par",
    "avec", "pour", "dans", "mais", "ou", "donc", "car",
    "tout", "plus", "bien", "comme", "avoir", "etre",
    "nous", "vous", "ils", "elles", "je", "tu", "il",
    "ceci", "cela", "cette", "ces", "mon", "ton",
    "message", "secret", "chiffre", "lettre", "texte",
    "allons", "enigma",
}


def score_dictionnaire(texte):
    """
    Compte le nombre de mots français reconnus dans le texte.
    Score plus élevé = texte plus probablement correct.
    """
    mots = texte.lower().split()
    return sum(1 for mot in mots if mot.strip(".,;:!?\"'") in MOTS_FRANCAIS)


def trouver_cle_naive(texte):
    """
    Casse le chiffrement Enigma par déchiffrage exhaustif + dictionnaire.

    Teste les 17 576 combinaisons (26³), déchiffre le texte pour chacune,
    retient la clé dont le texte contient le plus de mots français reconnus.

    Paramètre :
        texte (str) : le texte chiffré

    Retourne :
        tuple (tuple, str) : (clé (k1,k2,k3) trouvée, texte déchiffré)
        ou (None, None) si le texte est vide
    """
    nb = sum(1 for c in texte if utile.est_lettre(c))
    if nb == 0:
        return None, None
    if nb < 20:
        print(f"AVERTISSEMENT : seulement {nb} lettre(s) — résultat peu fiable.")

    meilleure_cle, meilleur_score, meilleur_texte = None, -1, ""

    for k1 in range(26):
        for k2 in range(26):
            for k3 in range(26):
                candidat = enigma.enigma_dechiffrer(texte, (k1, k2, k3))
                score = score_dictionnaire(candidat)
                if score > meilleur_score:
                    meilleur_score = score
                    meilleure_cle  = (k1, k2, k3)
                    meilleur_texte = candidat

    print("=== Résultat méthode naïve ===")
    print(f"Clé trouvée  : {meilleure_cle}")
    print(f"Score (mots) : {meilleur_score}  (mots français reconnus)")
    print("Message déchiffré :")
    print(meilleur_texte)

    return meilleure_cle, meilleur_texte


def mesurer_temps(texte, repetitions=3):
    """
    Mesure le temps d'exécution de trouver_cle_naive() via timeit.

    Paramètres :
        texte        (str) : texte chiffré
        repetitions  (int) : nombre de répétitions (défaut : 3)
                             ⚠ Garder bas — chaque appel fait 17 576 déchiffrages.

    Retourne :
        tuple (float, float) : (temps total, temps moyen par appel)
    """
    temps_total = timeit.timeit(
        stmt="trouver_cle_naive(texte)",
        globals={**globals(), "texte": texte},
        number=repetitions
    )
    temps_moyen = temps_total / repetitions

    print("\n=== Mesure de performance (Enigma — méthode naïve) ===")
    print(f"Répétitions : {repetitions}")
    print(f"Temps total : {temps_total:.4f} s")
    print(f"Temps moyen : {temps_moyen:.4f} s / appel  ({temps_moyen * 1000:.1f} ms)")

    return temps_total, temps_moyen


