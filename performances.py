# =============================================================================
# Evaluation des performances des algo
# =============================================================================

import timeit
import cesar
import Enigma
import casser_brute
import casser_cesar_naive
import casser_enigma
import casser_enigma_naive

def lancer_comparatif():
    print("=" * 70)
    print(" ÉVALUATION DES PERFORMANCES ALGORITHMIQUES ")
    print("=" * 70)

    # Un texte long garantit que les méthodes par dictionnaire et par
    # fréquences ont suffisamment de caractères pour réussir l'analyse.
    texte_clair = (
        "Ceci est un message secret suffisamment long pour permettre "
        "une analyse frequentielle efficace et comparer la puissance "
        "des algorithmes de notre equipe."
    )
    
    cle_cesar = 14
    cle_enigma = (7, 16, 9)

    # Chiffrement initial des données de test
    texte_cesar = cesar.cesar_chiffrer(texte_clair, cle_cesar)
    texte_enigma = Enigma.enigma_chiffrer(texte_clair, cle_enigma)

    print(f"Longueur du texte à traiter : {len(texte_clair)} caractères\n")

    # --- ÉVALUATION 1 : CÉSAR  ---
    print("-" * 70)
    print("1. CASSAGE CÉSAR (26 itérations)")
    print("-" * 70)
    
    # César methode naive
    temps_cesar_naif = timeit.timeit(
        lambda: casser_cesar_naive.trouver_cle_naive(texte_cesar), 
        number=100
    ) / 100
    print(f" [RÉSULTAT] César methode naive : {temps_cesar_naif * 1000:.4f} ms / exécution")

    # César Optimisé
    temps_cesar_opti = timeit.timeit(
        lambda: casser_brute.trouver_cle(texte_cesar), 
        number=100
    ) / 100
    print(f"[RÉSULTAT] César Optimisé (Chi²)   : {temps_cesar_opti * 1000:.4f} ms / exécution")


    # --- ÉVALUATION 2 : ENIGMA CÉSAR ---
    print("\n" + "-" * 70)
    print("2. CASSAGE ENIGMA CÉSAR")
    print("-" * 70)

    # Enigma Optimisé
    temps_enigma_opti = timeit.timeit(
        lambda: casser_enigma.brute_force_enigma(texte_enigma, mode_optimise=True), 
        number=10
    ) / 10
    print(f" [RÉSULTAT] Enigma Optimisé (78 tests) : {temps_enigma_opti * 1000:.4f} ms / exécution")

    # Enigma methode naive
    # On limite à 3 répétitions car la la metghode est très lente
    print(" Calcul de l'approche Enigma naïve en cours (patientez quelques secondes)...")
    temps_enigma_naif = timeit.timeit(
        lambda: casser_enigma_naive.trouver_cle_naive(texte_enigma), 
        number=3
    ) / 3
    print(f" [RÉSULTAT] Enigma naive    : {temps_enigma_naif:.4f} s / exécution")

    # --- SYNTHÈSE ---
    print("\n" + "=" * 70)
    print(" SYNTHÈSE DES DONNÉES DE PERFORMANCE ")
    print("=" * 70)
    # Affichage des temps pour chaque méthode
    print(f"César méthode naive  : {temps_cesar_naif * 1000:.4f} ms")
    print(f"César Optimisé (Chi²)      : {temps_cesar_opti * 1000:.4f} ms")
    print(f"Enigma Optimisé (78 tests) : {temps_enigma_opti * 1000:.4f} ms")
    print(f"Enigma méthode naive    : {temps_enigma_naif:.4f} s  (soit {temps_enigma_naif * 1000:.1f} ms)")
    
    print("=" * 70)
    
    if temps_enigma_opti > 0:
        ratio = temps_enigma_naif / temps_enigma_opti
        print(f"L'optimisation Enigma (Chi²) est environ {ratio:.0f} fois plus rapide")
        print("que la méthode naive.")
    print("=" * 70)

if __name__ == "__main__":
    lancer_comparatif()
