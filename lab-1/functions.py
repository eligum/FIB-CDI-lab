"""Lab1 code"""

from typing import List, Tuple
import numpy as np
import matplotlib as plt
import random


def source_from_text(text: str) -> List[Tuple[str, int]]:
    """Returns the frequency of each character in the string.
    """
    freq = {}
    for c in text:
        freq[c] = freq.get(c, 0) + 1

    return list(freq.items())


def histogram(text: str):
    """Draws a historgram of the characters in the string.
    """
    pass


def random_text(text: str, n: int) -> str:
    """Returns a string of length `n` of random character from `text`.
    """
    population = []
    weights = []
    for (k, v) in source_from_text(text):
        population.append(k)
        weights.append(v)

    return "".join(random.choices(population, weights, k=n))


def random_text_Markov(text: str, k: int, n: int) -> str:
    pass


text = "the quick brown fox jumped over the lazy dog"
text = "Setze jutges d'un jutjat mengen fetge d'un penjat."
print(random_text(text, 50))
