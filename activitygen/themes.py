from typing import List
import requests
import os
import random

predefined = {
  "christmas" : ["santa", "christmas tree", "reindeer", "present", "elf", "snowman", "bauble", "stocking", "christmas pudding", "turkey", "angel", "jesus", "evergreen", "sleigh"],
  "animals" : ["cow", "donkey", "horse", "rabbit", "tortoise", "sheep", "hippopotamus", "tiger", "dog", "snake", "aardvark", "cheetah", "meerkat", "monkey", "zebra", "cat", "lion", "chicken", "lizard"],
  "plants" : ["roses", "trees", "flowers", "blossom", "acorn", "agriculture", "leaf", "juniper", "moss", "forest", "wood", "pollen", "photosynthesis", "petal", "jungle", "fern", "flora"],
  "cities" : ["London", "New York", "Chicago", "Los Angeles", "Edinburgh", "Hong Kong", "Tokyo", "Amsterdam", "Berlin", "Singapore", "Sydney", "Melbourne", "Bangkok", "Dubai", "Milan", "Toronto", "Budapest", "Shanghai", "Bucharest"]
}

# The maximum length of a word in the word_bank, excluding spaces
DEFAULT_WORD_MAX_LENGTH = 16

# Change this one if you want more or less words to be returned from the model by default
WORDS_TO_SELECT = 50

def pick_words(theme: str, count=WORDS_TO_SELECT, allow_multiword=True, already_used=[], max_length=DEFAULT_WORD_MAX_LENGTH) -> List[str]:
  """
  Return a list of 'count' randomly selected words for given theme 'theme'.
  If 'allow_multiword' is false, selections consisting of multiple words (e.g., space-separated or hyphen-separated) will not be included.
  """
  
  if theme in predefined:
    word_bank = list(filter(lambda w: w not in already_used, predefined[theme]))
    return random.sample(word_bank, count)

  params = { 'theme' : theme, 
             'count' : str(count), 
             'allow_multiword' : str(allow_multiword),
             'already_used' : ','.join(already_used),
             'max_length' : str(max_length) }

  r = requests.get(os.environ['WORDS_API_URL'] + '/words', params = params)
  
  if r.status_code != 200:
    raise RuntimeError("Words API Failed: " + r.text)

  return r.json()
