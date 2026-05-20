# =============================================================================
# casser_brute_naive.py — Cassage naïf du chiffrement de César
# =============================================================================
# Méthode : déchiffrage exhaustif des 26 clés + comptage de mots français.
#
# Principe :
#   Pour chaque clé candidate (0 à 25), on déchiffre le texte entier,
#   puis on compte combien de mots d'un dictionnaire français courant
#   apparaissent dans le résultat. La clé qui maximise ce score est retenue.
#
#   Aucune statistique, aucune fréquence — juste du texte et des mots.
# =============================================================================

import timeit
import cesar
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
}


def score_dictionnaire(texte):
    """
    Compte le nombre de mots français reconnus dans le texte.
    Score plus élevé = texte plus probablement correct.

    La ponctuation collée aux mots est retirée avant la recherche.
    """
    mots = texte.lower().split()
    return sum(1 for mot in mots if mot.strip(".,;:!?\"'") in MOTS_FRANCAIS)


def trouver_cle_naive(texte):
    """
    Casse le chiffrement de César par déchiffrage exhaustif + dictionnaire.

    Teste les 26 clés, déchiffre le texte pour chacune, retient la clé
    dont le texte déchiffré contient le plus de mots français reconnus.

    Paramètre :
        texte (str) : le texte chiffré

    Retourne :
        tuple (int, str) : (clé trouvée, texte déchiffré)
        ou (None, None) si le texte est vide
    """
    nb_lettres = sum(1 for c in texte if utile.est_lettre(c))
    if nb_lettres == 0:
        return None, None
    if nb_lettres < 20:
        print(f"AVERTISSEMENT : seulement {nb_lettres} lettre(s) — résultat peu fiable.")

    meilleure_cle, meilleur_score, meilleur_texte = None, -1, ""

    for cle in range(26):
        candidat = cesar.cesar_dechiffrer(texte, cle)
        score = score_dictionnaire(candidat)
        if score > meilleur_score:
            meilleur_score  = score
            meilleure_cle   = cle
            meilleur_texte  = candidat

    print("=== Résultat méthode naïve ===")
    print(f"Clé trouvée    : {meilleure_cle}")
    print(f"Score (mots)   : {meilleur_score}  (mots français reconnus)")
    print("Message déchiffré :")
    print(meilleur_texte)

    return meilleure_cle, meilleur_texte


def mesurer_temps(texte, repetitions=200):
    """
    Mesure le temps d'exécution de trouver_cle_naive() via timeit.

    Paramètres :
        texte        (str) : texte chiffré
        repetitions  (int) : nombre de répétitions (défaut : 200)

    Retourne :
        tuple (float, float) : (temps total, temps moyen par appel)
    """
    temps_total = timeit.timeit(
        stmt="trouver_cle_naive(texte)",
        globals={**globals(), "texte": texte},
        number=repetitions
    )
    temps_moyen = temps_total / repetitions

    print("\n=== Mesure de performance (César — méthode naïve) ===")
    print(f"Répétitions : {repetitions}")
    print(f"Temps total : {temps_total:.4f} s")
    print(f"Temps moyen : {temps_moyen * 1000:.4f} ms / appel")

    return temps_total, temps_moyen


