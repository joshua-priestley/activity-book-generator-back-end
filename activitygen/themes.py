from typing import List
import requests
import os

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
  
  params = { 'theme' : theme, 
             'count' : str(count), 
             'allow_multiword' : str(allow_multiword),
             'already_used' : ','.join(already_used) }

  r = requests.get(os.environ['WORDS_API_URL'] + '/words', params = params)

  if r.status_code != 200:
    raise RuntimeError("Words API Failed: " + r.text)

  return r.json()
