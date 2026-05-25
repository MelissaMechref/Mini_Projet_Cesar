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
	# lstrip("-") enlève tous les tirets au début, pour distinguer :
	#   "-42" (entier négatif, pas de tiret après le signe)
	#   "7-16-9" (trois nombres séparés par des tirets)
	if "-" in texte.lstrip("-"):
		# Si oui, c'est une clé Enigma César : on coupe au niveau du "-" et on convertit en entiers.
		return tuple(int(x) for x in texte.split("-"))
	# Sinon, c'est une clé César simple : on convertit en entier.
	return int(texte)

def main(argv=None):
	"""Point d'entrée principal du programme en ligne de commande.

	Cette fonction :
	1. Parse les arguments saisis par l'utilisateur (action, message, clé)
	2. Convertit la clé en type approprié (int ou tuple)
	3. Appelle la fonction correspondante (chiffrer, dechiffrer ou enigma_chiffrer)
	4. Affiche le résultat

	Paramètre :
		argv (list ou None) : si None, utilise sys.argv (arguments de la console).
		                      si list, utilise les arguments fournis (utile pour les tests).

	Exemples d'utilisation en terminal :
		python main.py chiffrer "Veni, vidi, vici!" --cle 42
		python main.py dechiffrer "Ludy, lyty, lysy!" --cle 42
		python main.py enigma "MAISON" --cle 7-16-9
	"""
	# === ÉTAPE 1 : Créer et configurer le parseur d'arguments ===
	# argparse est un module qui aide à gérer les arguments en ligne de commande.
	# ArgumentParser crée un analyseur personnalisé pour notre programme.
	parser = argparse.ArgumentParser(
		description="Mini-Projet A : chiffrement de César / Enigma César.")

	# === ÉTAPE 2 : Définir les arguments attendus ===

	# Argument positionnel "action" : l'opération à effectuer.
	# - Obligatoire (pas de -- devant)
	# - Doit être l'une des valeurs listées dans "choices"
	parser.add_argument(
		"action",
		choices=["chiffrer", "dechiffrer", "enigma"],
		help="Opération à effectuer (chiffrer, dechiffrer ou enigma).")

	# Argument positionnel "message" : le texte à traiter.
	# - Obligatoire
	# - C'est la chaîne que nous allons chiffrer ou déchiffrer
	parser.add_argument(
		"message",
		help="Texte à traiter (mettez-le entre guillemets).")

	# Argument optionnel "--cle" (abréviation "-c") : la clé de chiffrement.
	# - Obligatoire via required=True
	# - Peut être un entier (César) ou trois entiers séparés par des tirets (Enigma César)
	parser.add_argument(
		"-c", "--cle", required=True,
		help="Clé : un entier (ex. '42') ou 'a-b-c' (ex. '7-16-9') pour Enigma.")

	# === ÉTAPE 3 : Analyser les arguments ===
	# parse_args() transforme les arguments en un objet "Namespace" avec des attributs.
	# Si argv=None, il lit automatiquement depuis la ligne de commande.
	# Sinon, il utilise la liste fournie.
	args = parser.parse_args(argv)

	# Maintenant, on peut accéder aux arguments via :
	# - args.action (ex. "chiffrer")
	# - args.message (ex. "Veni, vidi, vici!")
	# - args.cle (ex. "42" ou "7-16-9", toujours en chaîne de caractères)

	# === ÉTAPE 4 : Convertir la clé (texte) en type approprié ===
	# _parse_cle() transforme la clé en int (César) ou tuple (Enigma).
	cle = _parse_cle(args.cle)

	# === ÉTAPE 5 : Choisir et exécuter l'opération ===
	# Selon l'action, on appelle la fonction appropriée.
	# (Une fois que chiffrer / dechiffrer / enigma_chiffrer seront implémentées,
	#  ces appels retourneront le résultat du chiffrement/déchiffrement.)

	if args.action == "chiffrer":
		# L'utilisateur veut chiffrer : on appelle chiffrer()
		resultat = chiffrer(args.message, cle)
	elif args.action == "dechiffrer":
		# L'utilisateur veut déchiffrer : on appelle dechiffrer()
		resultat = dechiffrer(args.message, cle)
	else:  # args.action == "enigma"
		# L'utilisateur veut utiliser Enigma César : on appelle enigma_chiffrer()
		resultat = enigma_chiffrer(args.message, cle)

	# === ÉTAPE 6 : Afficher le résultat ===
	# print() affiche le résultat à l'écran pour que l'utilisateur le voie.
	print(resultat)
	
	# TODO : Une fois les fonctions de base implémentées, vous pourrez :
	# - Ajouter des options pour lire/écrire depuis des fichiers
	# - Implémenter le mode brute-force
	# - Ajouter d'autres fonctionnalités


if __name__ == "__main__":
	# Ce bloc s'exécute SEULEMENT si ce fichier est lancé directement depuis le terminal.
	# Exemple : python main.py chiffrer "Veni" --cle 42
	#
	# Il ne s'exécute PAS si on fait "import main" depuis un autre fichier Python.
	# Cela permet d'utiliser le code de main.py dans d'autres projets sans lancer main().
	# 
	# Pour les tests : pytest importe ce fichier mais ne lance pas main()
	# (car __name__ ne vaut pas "__main__" lors d'un import).
	main()

