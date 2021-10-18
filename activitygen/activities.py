import re
from flask import Blueprint, jsonify, request
from random import Random
from typing import List

NOT_LOWER_ALPHA = re.compile("([^a-z]+)")

bp = Blueprint("activities", __name__, url_prefix="/activities")

@bp.route("/anagrams")
def anagrams():
  words = request.args.getlist("words")
  return jsonify(generate_anagrams(words))

def generate_anagrams(words: List[str], seed=None) -> List[str]:
  anagrams: List[str] = []

  for word in words:
    split_words: List[str] = NOT_LOWER_ALPHA.split(word.lower())

    for i, split_word in enumerate(split_words):
      if NOT_LOWER_ALPHA.fullmatch(split_word):
        continue
      chars = list(split_word)
      Random(seed).shuffle(chars)
      split_words[i] = "".join(chars)

    anagrams.append("".join(split_words))
  
  return anagrams
