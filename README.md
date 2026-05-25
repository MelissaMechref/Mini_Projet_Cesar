# MGA802 — Mini-Projet A : Chiffrement de César et Enigma César

**École de Technologie Supérieure - Programmation Python (MGA802) - Été 2026**
Équipe : BLANCHARD Flavien · MECHREF Milissa · CONDETTE Vincent

---

## Description

Programme Python implémentant deux modes de chifferement par substitution :
- **César** - chaque lettre est décalée d'un entier fixe dans l'alphabet.
- **Enigma César** - variante cyclique : une clé de 3 entiers est appliquée tour à tour, lettre par lettre (inspiré de la machine Enigma).

Le programme chiffre et déchiffre des messages ou des fichiers `.txt`, et peut retrouver automatiquement la clé d'un message chiffré (**brute-force**) par deux méthodes : analyse fréquentielle ou naïve (mots fréquents).

---



## Structure du projet
```
mga802-miniprojeta/
⌈ main.py                  # Point d'entrée - fonctions + CLI (argparse)
⎮ interface.py             # Interface interactive 
⎮ cesar.py                 # Cesar_chiffrer(), cesar_dechiffrer()
⎮ enigma.py                # enigma_chiffrer(), enigma_dechiffrer()
⎮ utile.py                 # Constantes alphabet, fonctions utilitaires
⎮ gestion_fichier.py       # lire_fichier(), ecrire_fichier(), generer_nom_sortie()
⎮ casser_brute.py          # brute-force César - méthode d'analyse fréquentielle (26 tests)
⎮ casser_cesar_naive.py    # Brute-force César - méthode naïve (26 tests)
⎮ casser_enigma.py         # Brute-force Enigma - analyse fréquentielle optimisée (78 tests) ou exhaustif (17 576 tests)
⎮ casser_enigma_naive.py   # Brute-force Enigma - méthode naïve (17 576 tests)
⎮ message.txt              # Fichier texte d'exemple
⎮ requirements.txt         # Dépendance: pytest
└── tests/
    └── test_caesar.py     # 44 tests unitaires (pytest)
```
---
## Instalation

**Prérequis:** Python 3.1 ou supérieur

```bash
# 1. Cloner le dépôt
git clone <url-du-depot>
cd mga802-miniprojeta

# 2. Installer pytest (seule dépendance externe)
pip install -r requirements.txt
```

---

## Comment faire marcher le code

### 1. Chiffrement de César - message direct
```bash
python main.py chiffrer "Veni, vidi, vici!" --cle42
# -> Ludy, lity, lysy!

python main.py chiffrer "Veni, vidi, vici!" --cle -42
# -> Foxs, fsns, fsms!
```

### 2. Chiffrement Enigma César - message direct

La clé est composée de **3 entiers séparés par des tirets** (ex. `7-16-9`) :

```bsh
python main.py enigma "MAISON" --cle 7-16-9
# -> TQRZEW
```

### 3. Chiffrer / déchiffrer un fichier `.txt`
```bsh
# Chiffrer message.txt avec la clé 13 -> crée message_chiffre.txt
python main.py chiffrer --fichier message.txt --cle 13

# Déchiffrer le fichier produit -> crée message_chiffre_dechiffre.txt
python main.py dechiffrer --fichier message_chiffre.txt --cle 13

#Chiffrer un fichier avec Enigma -> crée message_enigma.txt
python main.py enigma --fichier message.txt --cle 7-16-9
```
> Les fichiers de sorties sont générés automatiquement dans le même dossier,
>  avec un suffixe ajouté au nom : `_chiffre`, `_dechiffre`, `_enigma`, `_casse`.

### 4. Brute-force - retroucer la clé automatiquement
```bsh
#César - méthode d'analyse fréquentielle (rapide)
python main.py brute --fichier message_chiffre.txt

#César - méthode naïve (mots fréquents)
python main.py brute --fichier message_chiffre.txt --naive

#Enigma - méthode d'analyse fréquentielle optimisée (78 tests, rapide)
python main.py brute --fichier message_chiffre.txt --enigma

#Enigma - méthode naïve (17 576 tests, lente)
python main.py brute --fichier message_chiffre.txt --enigma --naive
```

Le résultat déchiffré est enregistré dans `<nom_fichier>_casse.txt`.

### Option interface 

Lance un menu en terminal : 
```bash
python interface.py
```
 
Le menu propose :
 
```
  [1]  Chiffrer    --  Cesar
  [2]  Dechiffrer  --  Cesar
  [3]  Chiffrer    --  Enigma
  [4]  Dechiffrer  --  Enigma
  [6]  Casser      --  Cesar  (fréquentielle ou naïve)
  [7]  Casser      --  Enigma (fréquentielle ou naïve)
  [5]  Historique des operations
  [0]  Quitter
```
 
Pour chaque option, le programme demande le message et la clé, puis affiche le résultat.
L'option **Casser** tente de retrouver la clé automatiquement sans la connaître.
 


---

## Fonctionnement du code

### Chiffrement de César

Chaque lettre est décalée d'une valeur dans l'alphabet. La casse est préservée, la ponctuation et les espaces sont inchangés.

```
nouvelle_position = (position_originale + clé) % 26
```
La clé peut être **positive, négative, ou très grande** - le modulo 26 est toujours appliqué.

### Chiffrement Enigma César

La clé `(k1, k2, k3)`est appliquée **cycliquement sur les lettres uniquement** - les espaces et la ponctuation sont négligés donc ne font pas avancer l'index de clé.

| Position lettre | 1  | 2  | 3  | 4  | 5  | 6  |
|-----------------|----|----|----|----|----|----|
| Clé appliquée   | k1 | k2 | k3 | k1 | k2 | k3 |

**Exemple : **clé `(7, 16, 9)`sur `MAISON`-> `TQRZEW`

### Brute-force César (2 méthodes)

| Méthode | Tests | Principe |
|---------|-------|----------|
| **fréquence** (défaut) | 26 | Minimise l'écart avec les fréquences de lettres du français |
| **Naïve** (`--naive`) | 26 | Maximise le nombre de mots français reconnus |
 
### Brute-force Enigma (2 méthodes)

| Méthode | Tests | Principe |
|---------|-------|----------|
| **fréquence optimisée** (défaut) | 78 (3 × 26) | Analyse chaque position de clé séparément — ~225× plus rapide |
| **Naïve** (`--naive`) | 17 576 (26³) | Teste toutes les combinaisons, compte les mots français |

--- 

## Performances

Mesures réalisées avec `timeit`, texte de référence : 50 caractères.

| Méthode | Clés testées | Temps moyen |
|---|---|---|
| César — frequentielle | 26 | < 1 ms |
| César — naïve | 26 | < 1 ms |
| Enigma — frequentielle optimisé | 78 | ~5 ms |
| Enigma — frequentielle exhaustive | 17 576 | ~1-3 s |
| Enigma — naïve | 17 576 | ~2-5 s |

> Les temps varient selon la machine.

---

## Tests unitaires
```bash
# Lancer tous les tests (depuis la racine du projet)
pytest -v

# Si pytest n'est pas dans le PATH
python -m pytest -v

# Lancer un seul test
pytest -v tests/test_caesar.py::test_cesar_officiel_cle_42
```

**44 tests** au total — tous doivent afficher `PASSED` :

| Catégorie | Nombre | Ce qui est testé |
|---|---|---|
| César officiel | 5 | Cas de l'énoncé + round-trip + clé 0 |
| Chiffrement César | 14 | Majuscules, minuscules, ponctuation, clés limites, chaîne vide, bouclage, accents |
| Déchiffrement César | 5 | Cas officiel, clé 0, clé négative, chaîne vide, ponctuation |
| Enigma César | 11 | Cas officiel, round-trip, clé 0, `ValueError`, ponctuation sans avancer la clé, clés négatives/grandes |
| Brute-force César | 4 | frequentielle et naïve trouvent la bonne clé, texte vide |
| Brute-force Enigma | 4 | frequentielle optimisée et naïve trouvent la bonne clé, texte vide |







*Projet académique — École de Technologie Supérieure, MGA802, Été 2026.*

