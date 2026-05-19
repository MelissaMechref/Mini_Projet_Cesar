def lire_fichier(chemin):
    try:
        with open(chemin,"r",encoding="utf-8") as file:
            contenu = file.read()
            return conten
    except FileNotFoundError:
        print("ERREUR : Le fichier ", chemin, "n'existe pas")
        return None
    except Exception as erreur:
        print("Erreur inattendue : ",erreur)
        return None

def ecrire_fichier(chemin,contenu):
    try:
        with open(chemin,'w',encoding="utf-8") as file:
            file.write(contenu)
        print("Fichier enregistrer :",chemin)
        return True
    except PermissionError:
        print("ERREUR : Impossible d'écrire dans fichier : ",chemin)
        return False

def generer_nom_sortie(chemin_entree,suffixe):
    parties = chemin_entree.split(".")
    if len(parties) >=2:
        nom_base =".".join(parties[:-1])
        extension = parties[-1]
        return nom_base+suffixe+"."+extension
    else:
        return chemin_entree+suffixe

def fichier_existe(chemin):
    try:
        with open(chemin,"r") as file:
            return True
    except:
        return False