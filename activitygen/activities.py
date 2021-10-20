import re
from enum import Enum
from flask import Blueprint, jsonify, request
from functools import total_ordering
from random import getrandbits, Random
from typing import List
import word_search

NOT_LOWER_ALPHA = re.compile("([^a-z]+)")

@total_ordering
class Difficulty(Enum):
  EASY = 0
  MEDIUM = 1
  HARD = 2
  def __lt__(self, other):
    return self.value < other.value

bp = Blueprint("activities", __name__, url_prefix="/activities")

@bp.route("/anagrams")
def anagrams():
  words = request.args.getlist("words")
  difficulty = Difficulty[request.args.get("difficulty", Difficulty.HARD).upper()]
  return jsonify(generate_anagrams(words, difficulty))

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

      if recover_fixed:
        shuffled.insert(0, split_word[0])
        shuffled.append(split_word[-1])

      split_words[i] = "".join(shuffled)

    anagrams.append("".join(split_words))
  
  return anagrams

def generate_word_search(words, difficulty):
  # Find a way to split the words into the ones to use in the word search itself and
  # the hidden message. Also, the word search doesn't use difficulty (sorry)

  # word_search.generate(words, hidden_message)
  pass