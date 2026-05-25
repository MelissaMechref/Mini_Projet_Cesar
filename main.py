"""
MGA802 — Mini-Projet A : Chiffrement de César et Enigma César
"""
import argparse
from html import parser
import sys


import cesar
import enigma  
import casser_enigma 
import casser_cesar  

def chiffrer(message: str, cle: int):
	# Exigences visibles dans tests/test_caesar.py :
	# - test_cesar_officiel_cle_42
	# - test_cesar_officiel_cle_neg_42
	# - test_cesar_cle_zero_identite
	# Exemples attendus par les tests :
	# - chiffrer("Veni, vidi, vici!", 42) -> "Ludy, lyty, lysy!"
	# - chiffrer("Veni, vidi, vici!", -42) -> "Foxs, fsns, fsms!"
	# - chiffrer("Tout pareil.", 0) -> "Tout pareil."
	return cesar.cesar_chiffrer(message, cle)


def dechiffrer(message: str, cle: int):
	# Exigence visible dans tests/test_caesar.py :
	# - test_cesar_round_trip
	# Le test vérifie que dechiffrer(chiffrer(msg, 7), 7) == msg.
	return cesar.cesar_dechiffrer(message, cle)


def enigma_chiffrer(message: str, cles):
	# TODO: retourner la chaîne chiffrée Enigma César (type str).
	# Exigence visible dans tests/test_caesar.py :
	# - test_enigma_officiel_maison
	# Exemple attendu par le test :
	# - enigma_chiffrer("MAISON", (7, 16, 9)) -> "TQRZEW"
	return Enigma.enigma_chiffrer(message, cles)


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
    
 # 1. Configuration du parseur d'arguments
    parser = argparse.ArgumentParser(
        description="Mini-Projet A : chiffrement de César / Enigma César.")

    # Ajout de l'action bruteforce aux choix possibles
    parser.add_argument(
        "action",
        choices=["chiffrer", "dechiffrer", "enigma", "bruteforce"],
        help="Opération à effectuer (chiffrer, dechiffrer, enigma ou bruteforce).")

    parser.add_argument(
        "message",
        help="Texte à traiter.")

    # La clé n'est pas requise si l'action est bruteforce
    parser.add_argument(
        "-c", "--cle", required=False,
        help="Clé : un entier (ex. '42') ou 'a-b-c' (ex. '7-16-9') pour Enigma.")
        
    parser.add_argument(
        "-f", "--fichier", action="store_true",
        help="Indique que l'argument 'message' est un chemin de fichier texte à lire.")

    # Ajout d'une option pour préciser la méthode de bruteforce (César ou Enigma)
    parser.add_argument(
        "--mode", choices=["cesar", "enigma"], default="cesar",
        help="Mode de chiffrement utilisé.")
    
 # 2. Analyse des arguments
    args = parser.parse_args(argv)

    # 3. Gestion de l'option fichier : lire le contenu si le fichier est activé
    if args.fichier:
        contenu = cesar.lire_fichier(args.message) 
        if contenu is None:
            sys.exit(1) # Quitter si le fichier n'est pas lu
        texte_a_traiter = contenu
    else:
        texte_a_traiter = args.message

    # 4. Vérification et conversion de la clé
    if args.action != "bruteforce":
        if args.cle is None:
            parser.error("L'argument cle est requis pour chiffrer, dechiffrer ou enigma.")
        cle = _parse_cle(args.cle)

    # 5. Exécution de l'action choisie
    resultat = ""
    if args.action == "chiffrer":
        resultat = chiffrer(texte_a_traiter, cle)
    elif args.action == "dechiffrer":
        resultat = dechiffrer(texte_a_traiter, cle)
    elif args.action == "enigma":
        resultat = enigma_chiffrer(texte_a_traiter, cle)
    elif args.action == "bruteforce":
        if args.mode == "cesar":
            cle_trouvee, resultat = casser_brute.trouver_cle(texte_a_traiter)
        elif args.mode == "enigma":
            cle_trouvee, resultat = casser_enigma.brute_force_enigma(texte_a_traiter, mode_optimise=True)

    # 6. Affichage ou sauvegarde du résultat
    if args.fichier:
        chemin_sortie = cesar.generer_nom_sortie(args.message, f"_{args.action}")
        cesar.ecrire_fichier(chemin_sortie, resultat)
    else:
        print(resultat)


if __name__ == "__main__":
    main()

