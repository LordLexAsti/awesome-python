import matplotlib.pyplot as plt
import numpy as np

# --- Fonction pour vérifier si un nombre est premier ---
def is_prime(n):
    """Retourne True si n est premier, False sinon."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# --- Paramètres du graphique ---
max_x = 100  # Valeur maximale pour l'axe des x
max_y = 50   # Valeur maximale pour l'axe des y (nombre de tables de multiplication)

# --- Génération du graphique et des données ---
graph = np.zeros((max_y + 1, max_x + 1), dtype=int)
primes = []
prime_positions = []  # Liste pour stocker les positions (x, y) des nombres premiers
empty_cases_before_prime = [] # Liste pour stocker le nombre de cases vides avant chaque nombre premier

for y in range(1, max_y + 1):
    for x in range(1, max_x + 1):
        graph[y, x] = x * y
        if is_prime(x * y) and x * y not in primes:
            primes.append(x * y)
            prime_positions.append((x, y))

            # Comptage des cases vides avant l'apparition du nombre premier
            empty_cases = np.count_nonzero(graph[y, 1:x] == 0)
            empty_cases_before_prime.append((x * y, empty_cases))

primes.sort()
prime_positions.sort(key=lambda pos: pos[0])  # Tri des positions par x croissant

# --- Affichage du graphique initial ---
plt.figure(figsize=(15, 8))
plt.imshow(graph, cmap='viridis', origin='lower', aspect='auto')

# --- Mise en évidence des nombres premiers ---
for x, y in prime_positions:
    plt.scatter(x, y, color='red', s=50)

plt.xlabel("x (Nombre)")
plt.ylabel("y (Table de Multiplication)")
plt.title("Graphique des Tables de Multiplication Empilées")
plt.colorbar(label="Valeur")
plt.show()

# --- Analyse des écarts entre nombres premiers consécutifs ---
gaps = np.diff(primes)

print("Écarts entre nombres premiers consécutifs:", gaps)
print("Moyenne des écarts:", np.mean(gaps))
print("Écart-type des écarts:", np.std(gaps))

# --- Histogramme des écarts ---
plt.figure(figsize=(10, 5))
plt.hist(gaps, bins=20, edgecolor='black')
plt.xlabel("Écart entre Nombres Premiers Consécutifs")
plt.ylabel("Fréquence")
plt.title("Distribution des Écarts entre Nombres Premiers")
plt.show()

# --- Affichage des cases vides avant chaque nombre premier ---
print("\nCases vides avant chaque nombre premier (nombre premier, cases vides) :")
for prime, cases in empty_cases_before_prime:
    print(f"({prime}, {cases})")

# --- Analyse des cases vides ---
empty_cases_counts = [cases for _, cases in empty_cases_before_prime]
plt.figure(figsize=(10, 5))
plt.hist(empty_cases_counts, bins=20, edgecolor='black')
plt.xlabel("Nombre de Cases Vides Avant un Nombre Premier")
plt.ylabel("Fréquence")
plt.title("Distribution du Nombre de Cases Vides Avant un Nombre Premier")
plt.show()#!/usr/bin/env python
# coding: utf-8

"""
    The approach taken is explained below. I decided to do it simply.
    Initially I was considering parsing the data into some sort of
    structure and then generating an appropriate README. I am still
    considering doing it - but for now this should work. The only issue
    I see is that it only sorts the entries at the lowest level, and that
    the order of the top-level contents do not match the order of the actual
    entries.

    This could be extended by having nested blocks, sorting them recursively
    and flattening the end structure into a list of lines. Revision 2 maybe ^.^.
"""

def sort_blocks():
    # First, we load the current README into memory
    with open('README.md', 'r') as read_me_file:
        read_me = read_me_file.read()

    # Separating the 'table of contents' from the contents (blocks)
    table_of_contents = ''.join(read_me.split('- - -')[0])
    blocks = ''.join(read_me.split('- - -')[1]).split('\n# ')
    for i in range(len(blocks)):
        if i == 0:
            blocks[i] = blocks[i] + '\n'
        else:
            blocks[i] = '# ' + blocks[i] + '\n'

    # Sorting the libraries
    inner_blocks = sorted(blocks[0].split('##'))
    for i in range(1, len(inner_blocks)):
        if inner_blocks[i][0] != '#':
            inner_blocks[i] = '##' + inner_blocks[i]
    inner_blocks = ''.join(inner_blocks)

    # Replacing the non-sorted libraries by the sorted ones and gathering all at the final_README file
    blocks[0] = inner_blocks
    final_README = table_of_contents + '- - -' + ''.join(blocks)

    with open('README.md', 'w+') as sorted_file:
        sorted_file.write(final_README)

def main():
    # First, we load the current README into memory as an array of lines
    with open('README.md', 'r') as read_me_file:
        read_me = read_me_file.readlines()

    # Then we cluster the lines together as blocks
    # Each block represents a collection of lines that should be sorted
    # This was done by assuming only links ([...](...)) are meant to be sorted
    # Clustering is done by indentation
    blocks = []
    last_indent = None
    for line in read_me:
        s_line = line.lstrip()
        indent = len(line) - len(s_line)

        if any([s_line.startswith(s) for s in ['* [', '- [']]):
            if indent == last_indent:
                blocks[-1].append(line)
            else:
                blocks.append([line])
            last_indent = indent
        else:
            blocks.append([line])
            last_indent = None

    with open('README.md', 'w+') as sorted_file:
        # Then all of the blocks are sorted individually
        blocks = [
            ''.join(sorted(block, key=str.lower)) for block in blocks
        ]
        # And the result is written back to README.md
        sorted_file.write(''.join(blocks))

    # Then we call the sorting method
    sort_blocks()


if __name__ == "__main__":
    main()
