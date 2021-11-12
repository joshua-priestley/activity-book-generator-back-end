import re
from flask import Blueprint, render_template, request
from random import getrandbits, Random
from typing import Dict, List

from .commons import Difficulty
from .themes import pick_words

NOT_LOWER_ALPHA = re.compile("([^a-z]+)")

bp = Blueprint("anagrams", __name__, url_prefix="/activities/anagrams")

@bp.route("/state")
def get_state():
  """Returns internal anagrams state from provided options"""
  theme = request.args.get("theme", "christmas")
  difficulty = Difficulty.from_str(request.args.get("difficulty"), Difficulty.HARD)
  print(f"Difficulty: {difficulty}")
  count = int(request.args.get("count", 10))

  words = pick_words(theme, count)

  return {
    "description": [f"The following words have been scrambled! Can you rearrange the letters to find each {theme} themed word?"],
    **generate_data(theme, words, difficulty)
  }

def generate_html(anagrams_data: Dict) -> str:
  """Generates HTML from internal data representation of anagrams"""
  blanks = (re.sub("[a-z]", "_", word) for word in anagrams_data["words"])
  return render_template("anagrams.html", theme=anagrams_data["theme"], data=zip(anagrams_data["anagrams"], blanks))

def generate_data(theme: str, words: List[str], difficulty: Difficulty) -> Dict:
  """Generates internal data representation of anagrams with the provided words"""
  return {
    "theme": theme,
    "words": words,
    "anagrams": generate_anagrams(words, difficulty)
  }

def generate_anagrams(words: List[str], difficulty: Difficulty, seed=None) -> List[str]:
  anagrams: List[str] = []

  for word in words:
    split_words: List[str] = NOT_LOWER_ALPHA.split(word.lower())

    for i, split_word in enumerate(split_words):
      if NOT_LOWER_ALPHA.fullmatch(split_word):
        continue
      chars = list(split_word)

      if difficulty == Difficulty.EASY and len(chars) > 3:
        # For easy difficulty (and len > 3): fix first and last characters
        # We exclude them from shuffle and add them back at the end
        chars = chars[1:-1]
        recover_fixed = True
      else:
        recover_fixed = False

      if difficulty <= Difficulty.MEDIUM and len(chars) > 3:
        # For easy and medium difficulty (and len > 3): group pairs of characters

        # There are two ways to group pairs (e.g., "he ll o" or "h el lo")
        # Randomly pick between them with 50-50 probability
        prefix = []
        if bool(getrandbits(1)):
          prefix.append(chars.pop(0))

        grouped_chars = [c1 + c2 for c1, c2 in zip(chars[::2], chars[1::2])]
        if len(chars) % 2 == 1:
          grouped_chars.append(chars[-1])
        chars = prefix + grouped_chars

      # Shuffle until different
      if len(chars) > 1:
        original = list(range(len(chars)))
        permutation = original
        while permutation == original:
          permutation = Random(seed).sample(original, len(original))
        shuffled = [chars[i] for i in permutation]
      else:
        shuffled = chars

      if recover_fixed:
        shuffled.insert(0, split_word[0])
        shuffled.append(split_word[-1])

      split_words[i] = "".join(shuffled)

    anagrams.append("".join(split_words))
  
  return anagrams
