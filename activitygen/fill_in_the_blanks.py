from .anagrams import Difficulty
from random import Random
from typing import Dict, List

# (min, max) proportion of letters to blank out, based on difficulty
letters_to_blank = {
  Difficulty.EASY: (1 / 10, 1 / 6),
  Difficulty.MEDIUM: (1 / 5, 1 / 3),
  Difficulty.HARD: (1 / 3, 1 / 2)
}

def generate(theme: str, words: List[str], difficulty: Difficulty) -> Dict:
  return {
    "theme": theme,
    "words": words,
    "blanked words": [blank_word(word, difficulty) for word in words]
  }

def blank_word(word: str, difficulty: Difficulty, seed=None) -> str:
  rng = Random(seed)

  # Only blank out letters
  letter_indices = [i for i in range(len(word)) if word[i].isalpha()]

  min_prop_to_blank, max_prop_to_blank = letters_to_blank[difficulty]
  min_to_blank = max(round(min_prop_to_blank * len(word)), 1)
  max_to_blank = max(min(round(max_prop_to_blank * len(word)), len(word) - 1), min_to_blank)
  print(f"{word}: ({min_to_blank}, {max_to_blank})")
  to_blank = rng.randint(min_to_blank, max_to_blank)
  indices_to_blank = rng.sample(letter_indices, to_blank)

  chars = list(word)
  for index in indices_to_blank:
    chars[index] = "_"
  return "".join(chars)
