# =============================================================================
# interface.py — Interface terminal pour le chiffrement César & Enigma
# =============================================================================
# Ce fichier gère toute l'interaction avec l'utilisateur.
# Il n'effectue aucun calcul — il délègue tout à :
#   - cesar.py               : chiffrement/déchiffrement César
#   - enigma.py              : chiffrement/déchiffrement Enigma
#   - casser_brute.py        : cassage César par fréquences (Chi²)
#   - casser_cesar_naive.py  : cassage César par dictionnaire de mots
#   - casser_enigma.py       : cassage Enigma par fréquences (Chi²)
#   - casser_enigma_naive.py : cassage Enigma par dictionnaire de mots
#
# Structure du fichier :
#   1. Imports
#   2. Constantes d'affichage
#   3. Fonctions d'affichage
#   4. Fonctions de saisie
#   5. Actions du menu
#   6. Boucle principale
# =============================================================================

import cesar
import enigma
import casser_cesar
import casser_cesar_naive
import casser_enigma
import casser_enigma_naive


# =============================================================================
# CONSTANTES D'AFFICHAGE
# =============================================================================

LARGEUR = 60  # Largeur fixe des séparateurs en nombre de caractères


# =============================================================================
# FONCTIONS D'AFFICHAGE
# =============================================================================

def ligne(char="─"):
    """Affiche une ligne horizontale de séparation."""
    print(char * LARGEUR)


def centrer(texte):
    """Affiche un texte centré sur la largeur définie."""
    print(texte.center(LARGEUR))


def afficher_menu():
    """
    Affiche le menu principal avec toutes les options disponibles.
    Appelée à chaque tour de la boucle principale.
    """
    print("\n" * 3)
    ligne("=")
    centrer("CHIFFREMENT CESAR & ENIGMA")
    ligne("=")
    print()

    # --- Chiffrement / Déchiffrement ---
    print("  [1]  Chiffrer    --  Cesar")
    print("  [2]  Dechiffrer  --  Cesar")
    print("  [3]  Chiffrer    --  Enigma")
    print("  [4]  Dechiffrer  --  Enigma")
    print()

    # --- Cassage automatique ---
    # Ces options tentent de retrouver la clé sans la connaître
    print("  [6]  Casser  --  Cesar  (methode frequentielle ou naive)")
    print("  [7]  Casser  --  Enigma (methode frequentielle ou naive)")
    print()

    # --- Utilitaires ---
    print("  [5]  Historique des operations")
    print("  [0]  Quitter")
    print()
    ligne()
    print()


def afficher_resultat(operation, msg_original, resultat, cle):
    """
    Affiche le résultat d'un chiffrement ou déchiffrement.

    Paramètres :
        operation    (str) : nom de l'opération, ex: "Chiffrement Cesar"
        msg_original (str) : le message saisi par l'utilisateur
        resultat     (str) : le message après chiffrement/déchiffrement
        cle               : la clé utilisée (int pour César, tuple pour Enigma)
    """
    print()
    ligne()
    centrer(f"[ {operation} ]")
    ligne()
    print(f"  Cle             : {cle}")
    print(f"  Message original: {msg_original}")
    print(f"  Resultat        : {resultat}")
    ligne()
    print()


def afficher_resultat_cassage(operation, msg_original, cle_trouvee, msg_dechiffre):
    """
    Affiche le résultat d'un cassage automatique.
    Similaire à afficher_resultat mais avec un libellé adapté au cassage.

    Paramètres :
        operation      (str) : nom de la méthode utilisée
        msg_original   (str) : le message chiffré soumis
        cle_trouvee         : la clé trouvée automatiquement
        msg_dechiffre  (str) : le message déchiffré avec cette clé
    """
    print()
    ligne()
    centrer(f"[ {operation} ]")
    ligne()
    print(f"  Message chiffre  : {msg_original}")
    print(f"  Cle trouvee      : {cle_trouvee}")
    print(f"  Message dechiffre: {msg_dechiffre}")
    ligne()
    print()


def afficher_erreur(msg):
    """Affiche un message d'erreur pour signaler une saisie invalide."""
    print(f"\n  ERREUR : {msg}\n")


def titre_section(texte):
    """Affiche un titre de section encadré entre deux lignes."""
    print()
    ligne()
    centrer(texte)
    ligne()
    print()


def attendre():
    """Pause : attend que l'utilisateur appuie sur Entrée avant de continuer."""
    input("  Appuyez sur Entree pour continuer... ")


# =============================================================================
# FONCTIONS DE SAISIE
# Chaque fonction boucle jusqu'à obtenir une saisie valide.
# =============================================================================

def demander_message():
    """
    Demande un message non vide à l'utilisateur.

    Retourne :
        str : le message saisi
    """
    while True:
        msg = input("  Message : ").strip()
        if msg:
            return msg
        afficher_erreur("Le message ne peut pas etre vide.")


def demander_cle_cesar():
    """
    Demande une clé entière (positive ou négative) pour César.

    Retourne :
        int : la clé saisie
    """
    while True:
        raw = input("  Cle Cesar (entier, ex: 42 ou -7) : ").strip()
        try:
            return int(raw)
        except ValueError:
            afficher_erreur("Entrez un nombre entier.")


def demander_cle_enigma():
    """
    Demande une clé Enigma : 3 entiers séparés par des espaces.
    Exemple valide : "7 16 9"

    Retourne :
        tuple (int, int, int) : les 3 clés
    """
    while True:
        raw = input("  Cle Enigma (3 entiers separes par espaces, ex: 7 16 9) : ").strip()
        parts = raw.split()  # Découpe la chaîne selon les espaces
        if len(parts) == 3:
            try:
                return tuple(int(p) for p in parts)
            except ValueError:
                pass
        afficher_erreur("Entrez exactement 3 entiers separes par des espaces.")


def demander_methode_cassage():
    """
    Demande à l'utilisateur quelle méthode de cassage utiliser :
      - Chi²  : analyse statistique des fréquences de lettres (plus fiable)
      - Naive : compte les mots français reconnus dans le texte (plus simple)

    Retourne :
        str : "1" pour Chi², "2" pour naive
    """
    print("  Quelle methode de cassage ?")
    print("  [1]  frequentielle -- analyse de frequences (recommande)")
    print("  [2]  Naive -- comptage de mots francais")
    print()
    while True:
        choix = input("  Votre choix [1-2] : ").strip()
        if choix in ("1", "2"):
            return choix
        afficher_erreur("Entrez 1 ou 2.")


# =============================================================================
# ACTIONS DU MENU
# Une fonction par option. Chaque action :
#   1. Affiche un titre
#   2. Demande les infos nécessaires
#   3. Appelle le module correspondant
#   4. Affiche le résultat
#   5. Ajoute à l'historique
# =============================================================================

def action_cesar_chiffrer(historique):
    """Chiffre un message avec l'algorithme de César."""
    titre_section("CESAR -- Chiffrer")
    msg = demander_message()
    cle = demander_cle_cesar()
    resultat = cesar.cesar_chiffrer(msg, cle)
    afficher_resultat("Chiffrement Cesar", msg, resultat, cle)
    historique.append(("Cesar chiffrer", str(cle), msg, resultat))


def action_cesar_dechiffrer(historique):
    """Déchiffre un message chiffré par César."""
    titre_section("CESAR -- Dechiffrer")
    msg = demander_message()
    cle = demander_cle_cesar()
    resultat = cesar.cesar_dechiffrer(msg, cle)
    afficher_resultat("Dechiffrement Cesar", msg, resultat, cle)
    historique.append(("Cesar dechiffrer", str(cle), msg, resultat))


def action_enigma_chiffrer(historique):
    """Chiffre un message avec Enigma César (3 clés en rotation)."""
    titre_section("ENIGMA -- Chiffrer")
    msg = demander_message()
    cles = demander_cle_enigma()
    resultat = enigma.enigma_chiffrer(msg, cles)
    afficher_resultat("Chiffrement Enigma", msg, resultat, cles)
    historique.append(("Enigma chiffrer", str(cles), msg, resultat))


def action_enigma_dechiffrer(historique):
    """Déchiffre un message chiffré par Enigma César."""
    titre_section("ENIGMA -- Dechiffrer")
    msg = demander_message()
    cles = demander_cle_enigma()
    resultat = enigma.enigma_dechiffrer(msg, cles)
    afficher_resultat("Dechiffrement Enigma", msg, resultat, cles)
    historique.append(("Enigma dechiffrer", str(cles), msg, resultat))


def action_casser_cesar(historique):
    """
    Tente de retrouver automatiquement la clé d'un message chiffré par César.

    Deux méthodes disponibles :
      - Chi²  : teste les 26 clés, garde celle dont la distribution de lettres
                ressemble le plus au français (score Chi-carré minimal).
                Délègue à casser_brute.py → trouver_cle()
      - Naive : teste les 26 clés, garde celle dont le texte contient le plus
                de mots français reconnus.
                Délègue à casser_cesar_naive.py → trouver_cle_naive()
    """
    titre_section("CASSER -- Cesar")
    msg = demander_message()
    print()
    methode = demander_methode_cassage()

    print()
    print("  Analyse en cours...")
    print()

    if methode == "1":
        # Méthode Chi² — plus fiable sur les textes longs
        cle, dechiffre = casser_brute.trouver_cle(msg)
        nom_methode = "Cassage Cesar (Chi²)"
    else:
        # Méthode naive — basée sur un dictionnaire de mots français courants
        cle, dechiffre = casser_cesar_naive.trouver_cle_naive(msg)
        nom_methode = "Cassage Cesar (naive)"

    # Si le cassage a échoué (texte trop court ou vide)
    if cle is None:
        afficher_erreur("Impossible de casser le message (pas assez de lettres).")
        return

    afficher_resultat_cassage(nom_methode, msg, cle, dechiffre)
    historique.append((nom_methode, str(cle), msg, dechiffre))


def action_casser_enigma(historique):
    """
    Tente de retrouver automatiquement la clé d'un message chiffré par Enigma.

    Deux méthodes disponibles :
      - Frequentielle  : analyse les fréquences de lettres séparément pour chaque
                position de clé (optimisé : 78 tests au lieu de 17 576).
                Délègue à casser_enigma.py → brute_force_enigma()
      - Naive : teste toutes les 26³ = 17 576 combinaisons possibles et
                compte les mots français reconnus dans chaque résultat.
                Délègue à casser_enigma_naive.py → trouver_cle_naive()
                ⚠ Beaucoup plus lent — prévoir plusieurs secondes.
    """
    titre_section("CASSER -- Enigma")
    msg = demander_message()
    print()
    methode = demander_methode_cassage()

    print()
    if methode == "2":
        # Prévenir l'utilisateur : 17 576 combinaisons à tester
        print("  Attention : la methode naive teste 17 576 combinaisons.")
        print("  Cela peut prendre plusieurs secondes...")
    else:
        print("  Analyse en cours (methode optimisee, 78 tests)...")
    print()

    if methode == "1":
        # Méthode Chi² optimisée : analyse chaque position de clé séparément
        cle, dechiffre = casser_enigma.brute_force_enigma(msg, mode_optimise=True)
        nom_methode = "Cassage Enigma (Chi²)"
    else:
        # Méthode naive : force brute sur toutes les combinaisons
        cle, dechiffre = casser_enigma_naive.trouver_cle_naive(msg)
        nom_methode = "Cassage Enigma (naive)"

    if cle is None:
        afficher_erreur("Impossible de casser le message (pas assez de lettres).")
        return

    afficher_resultat_cassage(nom_methode, msg, cle, dechiffre)
    historique.append((nom_methode, str(cle), msg, dechiffre))


def action_historique(historique):
    """
    Affiche toutes les opérations effectuées depuis le lancement.
    L'historique se remet à zéro à chaque fermeture du programme.
    """
    titre_section("HISTORIQUE DES OPERATIONS")

    if not historique:
        print("  Aucune operation effectuee pour l'instant.")
        print()
        return

    col_op  = 22
    col_cle = 12
    col_msg = 14
    col_res = 14
    total   = col_op + col_cle + col_msg + col_res + 10

    # En-tête du tableau
    print(f"  {'#':>3}  {'Operation':<{col_op}}  {'Cle':<{col_cle}}  {'Original':<{col_msg}}  {'Resultat':<{col_res}}")
    print("  " + "-" * total)

    for i, (op, cle, original, resultat) in enumerate(historique, 1):
        # [:col_msg] tronque les textes trop longs pour garder le tableau lisible
        print(
            f"  {i:>3}.  "
            f"{op:<{col_op}}  "
            f"{cle:<{col_cle}}  "
            f"{original[:col_msg]:<{col_msg}}  "
            f"{resultat[:col_res]:<{col_res}}"
        )
    print()


# =============================================================================
# BOUCLE PRINCIPALE
# =============================================================================

def main():
    """
    Boucle principale du programme.

    Fonctionnement :
        1. Affiche le menu
        2. Lit le choix de l'utilisateur
        3. Appelle la fonction correspondante
        4. Répète jusqu'à ce que l'utilisateur tape 0
    """
    # L'historique est une liste de tuples partagée entre toutes les actions.
    # Format : (nom_operation, cle, message_original, resultat)
    historique = []

    # Dictionnaire choix → fonction : plus propre qu'une série de if/elif
    actions = {
        "1": action_cesar_chiffrer,
        "2": action_cesar_dechiffrer,
        "3": action_enigma_chiffrer,
        "4": action_enigma_dechiffrer,
        "5": action_historique,
        "6": action_casser_cesar,
        "7": action_casser_enigma,
    }

    while True:
        afficher_menu()
        choix = input("  Votre choix [0-7] : ").strip()

        if choix == "0":
            print()
            centrer("A bientot !")
            print()
            return  # Termine proprement sans forcer la fermeture

        if choix not in actions:
            afficher_erreur("Choix invalide, entrez un nombre entre 0 et 7.")
            attendre()
            continue  # Retourne au début du while directement

        print()
        actions[choix](historique)
        attendre()


if __name__ == "__main__":
    main()
