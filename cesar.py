# =============================================================================
# cesar.py — Chiffrement et déchiffrement de César
# =============================================================================

import utile
from utile import ALPHABET_LEN


def decaler_caractere(caractere, decalage):
    """
    Décale un seul caractère de l'alphabet selon la clé de César.
    Les caractères non alphabétiques (espaces, ponctuation, chiffres) sont
    retournés sans modification.

    Paramètres :
        caractere (str) : le caractère à décaler
        decalage  (int) : le nombre de positions à décaler (positif ou négatif)

    Retourne :
        str : le caractère décalé (ou inchangé s'il n'est pas une lettre)
    """
    # Si ce n'est pas une lettre, on ne touche pas au caractère
    if not utile.est_lettre(caractere):
        return caractere

    # Récupère la position dans l'alphabet (0-25)
    index_origine = utile.index_lettre(caractere)

    # Calcule le nouvel index en appliquant le décalage + modulo pour rester dans 0-25
    nouvel_index = (index_origine + decalage) % ALPHABET_LEN

    # Retourne la lettre correspondante en conservant la casse d'origine
    return utile.lettre_depuis_index(nouvel_index, caractere)


def cesar_chiffrer_rapide(texte, cle):
    """
    Chiffre un texte selon le chiffrement de César.

    Cette version simple parcourt chaque caractère et applique le décalage.

    Paramètres :
        texte (str) : le texte à chiffrer
        cle   (int) : la clé de chiffrement (décalage)

    Retourne :
        str : le texte chiffré
    """
    resultat = []
    for caractere in texte:
        resultat.append(decaler_caractere(caractere, cle))
    return ''.join(resultat)
