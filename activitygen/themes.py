import random
import re
from typing import List

ALPHABETIC = re.compile(r"[a-zA-Z]+")

themes = {
  "christmas" : ["santa", "christmas tree", "reindeer", "present", "elf", "snowman", "bauble", "stocking", "christmas pudding", "turkey", "angel", "jesus", "evergreen", "sleigh"],
  "animals" : ["cow", "donkey", "horse", "rabbit", "tortoise", "sheep", "hippopotamus", "tiger", "dog", "snake", "aardvark", "cheetah", "meerkat", "monkey", "zebra", "cat", "lion", "chicken", "lizard"],
  "plants" : ["roses", "trees", "flowers", "blossom", "acorn", "agriculture", "leaf", "juniper", "moss", "forest", "wood", "pollen", "photosynthesis", "petal", "jungle", "fern", "flora"],
  "cities" : ["london", "new york", "chicago", "los angeles", "edinburgh", "hong kong", "tokyo", "singapore", "amsterdam", "berlin", "singapore", "sydney", "melbourne", "bangkok", "dubai", "milan", "toronto", "budapest", "shanghai"]
}

def pick_words(theme: str, count: int, allow_multiword=True, already_used=[]) -> List[str]:
  """
  Return a list of 'count' randomly selected words for given theme 'theme'.
  If 'allow_multiword' is false, selections consisting of multiple words (e.g., space-separated or hyphen-separated) will not be included.
  """
  word_bank = themes[theme]
  if not allow_multiword:
    word_bank = list(filter(ALPHABETIC.fullmatch, word_bank))

  word_bank = list(filter(lambda w: w not in already_used, word_bank))

  words = random.sample(word_bank, count)
  return words
