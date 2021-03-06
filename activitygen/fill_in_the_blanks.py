from flask import Blueprint, render_template, request
from random import Random
from typing import Dict, List

from .commons.difficulty import Difficulty
from .themes import pick_words

# (min, max) proportion of letters to blank out, based on difficulty
letters_to_blank = {
  Difficulty.EASY: (1 / 10, 1 / 6),
  Difficulty.MEDIUM: (1 / 5, 1 / 3),
  Difficulty.HARD: (1 / 3, 1 / 2)
}

bp = Blueprint("fill-in-the-blanks", __name__, url_prefix="/activities/fill-in-the-blanks")

@bp.route("/state")
def get_state():
  """Returns internal fill in the blanks state from provided options"""
  # TODO: Remove theme from here and pass it around on the frontend. It has no purpose in the backend
  theme = request.args.get("theme", "christmas")
  
  difficulty = Difficulty.from_str(request.args.get("difficulty"), Difficulty.HARD)
  words = request.args.get("words").split(",")

  return {
    "description": f"Some letters from the following words are missing! Can you fill in the blanks to complete each {theme} themed word?",
    **generate(theme, words, difficulty)
  }

def generate_html(fill_in_the_blanks_data: Dict):
  """Generates HTML from internal data representation of Fill In the Blanks"""
  return render_template("fill_in_the_blanks.html",
                         theme=fill_in_the_blanks_data["theme"],
                         blanked_words=fill_in_the_blanks_data["blanked_words"])

def generate(theme: str, words: List[str], difficulty: Difficulty) -> Dict:
  """Generates internal data representation of anagrams with the provided words"""
  return {
    "theme": theme,
    "words": words,
    "blanked_words": [blank_word(word, difficulty) for word in words]
  }

def blank_word(word: str, difficulty: Difficulty, seed=None) -> str:
  rng = Random(seed)

  # Only blank out letters
  letter_indices = [i for i in range(len(word)) if word[i].isalpha()]

  min_prop_to_blank, max_prop_to_blank = letters_to_blank[difficulty]
  min_to_blank = max(round(min_prop_to_blank * len(word)), 1)
  max_to_blank = max(min(round(max_prop_to_blank * len(word)), len(word) - 1), min_to_blank)
  to_blank = rng.randint(min_to_blank, max_to_blank)
  indices_to_blank = rng.sample(letter_indices, to_blank)

  chars = list(word)
  for index in indices_to_blank:
    chars[index] = "_"
  return "".join(chars)
