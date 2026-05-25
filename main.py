"""
MGA802 — Mini-Projet A : Chiffrement de César
"""
import argparse
import cesar
import enigma


def chiffrer(message: str, cle: int) -> str:
    """
    Chiffre un message avec le chiffrement de César.

    Paramètres :
        message (str) : le texte à chiffrer
        cle     (int) : le décalage (positif ou négatif)

    Retourne :
        str : le texte chiffré
    """
    return cesar.cesar_chiffrer(message, cle)


def dechiffrer(message: str, cle: int) -> str:
    """
    Déchiffre un message chiffré par César.

    Paramètres :
        message (str) : le texte chiffré
        cle     (int) : la clé utilisée lors du chiffrement

    Retourne :
        str : le texte déchiffré
    """
    return cesar.cesar_dechiffrer(message, cle)


def enigma_chiffrer(message: str, cles) -> str:
    """
    Chiffre un message avec le chiffrement Enigma César (3 clés en rotation).

    Paramètres :
        message (str)        : le texte à chiffrer
        cles    (tuple[int]) : triplet de clés (k1, k2, k3)

    Retourne :
        str : le texte chiffré
    """
    return enigma.enigma_chiffrer(message, cles)


def _parse_cle(texte: str):
    """Convertit l'argument --cle en clé utilisable.

    Cette fonction analyse la clé fournie par l'utilisateur en ligne de commande
    et la transforme en type Python approprié :
    - César           : un entier, ex. "42" ou "-42"
    - Enigma César    : trois entiers séparés par des tirets, ex. "7-16-9"

    Paramètre :
        texte (str) : la chaîne saisie par l'utilisateur après --cle.

    Retour :
        int : une clé entière pour César
        tuple : un tuple de 3 entiers pour Enigma César

    Exemple :
        _parse_cle("42") → 42 (int)
        _parse_cle("7-16-9") → (7, 16, 9) (tuple)
    """
    # Vérifier s'il y a un tiret dans la clé (sauf si c'est juste un signe négatif).
    if "-" in texte.lstrip("-"):
        return tuple(int(x) for x in texte.split("-"))
    return int(texte)


def main(argv=None):
    """Point d'entrée principal du programme en ligne de commande.

    Exemples d'utilisation en terminal :
        python main.py chiffrer "Veni, vidi, vici!" --cle 42
        python main.py dechiffrer "Ludy, lyty, lysy!" --cle 42
        python main.py enigma "MAISON" --cle 7-16-9
    """
    parser = argparse.ArgumentParser(
        description="Mini-Projet A : chiffrement de César / Enigma César.")

    parser.add_argument(
        "action",
        choices=["chiffrer", "dechiffrer", "enigma"],
        help="Opération à effectuer (chiffrer, dechiffrer ou enigma).")

    parser.add_argument(
        "message",
        help="Texte à traiter (mettez-le entre guillemets).")

    parser.add_argument(
        "-c", "--cle", required=True,
        help="Clé : un entier (ex. '42') ou 'a-b-c' (ex. '7-16-9') pour Enigma.")

    args = parser.parse_args(argv)

    cle = _parse_cle(args.cle)

    if args.action == "chiffrer":
        resultat = chiffrer(args.message, cle)
    elif args.action == "dechiffrer":
        resultat = dechiffrer(args.message, cle)
    else:  # args.action == "enigma"
        resultat = enigma_chiffrer(args.message, cle)

    print(resultat)


if __name__ == "__main__":
    main()
