from typing import List
import requests
import os

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
