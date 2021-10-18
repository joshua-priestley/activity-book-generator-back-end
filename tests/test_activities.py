import pytest
from activitygen.activities import Difficulty, generate_anagrams
from collections import Counter

@pytest.mark.parametrize("difficulty", (Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD))
def test_anagram_gen_gives_rearrangement(difficulty):
  """Anagrams should use exactly the same characters as the original strings"""
  sample_words = ["cow", "reindeer", "skeleton", "princess", "christmas tree", "a", "tv"]
  assert all(is_rearrangement(word, anagram)
             for word, anagram in zip(sample_words, generate_anagrams(sample_words, difficulty)))

@pytest.mark.parametrize("difficulty", (Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD))
def test_anagram_gen_makes_lowercase(difficulty):
  """Uppercase letters should be made lowercase"""
  sample_words = ["London Eye", "LiON"]
  assert all(anagram.islower() for anagram in generate_anagrams(sample_words, difficulty))

@pytest.mark.parametrize("difficulty", (Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD))
def test_anagram_gen_preserves_words(difficulty):
  """Letters from different words in the same string should not be mixed"""
  xmas_word, jacko_word = "christmas tree", "jack-o'-lantern"
  xmas_anagram, jacko_anagram = generate_anagrams([xmas_word, jacko_word], difficulty)

  assert is_rearrangement(xmas_word[:9], xmas_anagram[:9])
  assert xmas_anagram[9] == " "
  assert is_rearrangement(xmas_word[10:], xmas_anagram[10:])

  assert is_rearrangement(jacko_word[:4], jacko_anagram[:4])
  assert jacko_anagram[4] == "-"
  assert jacko_anagram[6:8] == "'-"
  assert is_rearrangement(jacko_word[8:], jacko_anagram[8:])

def is_rearrangement(str1: str, str2: str) -> bool:
  return Counter(str1) == Counter(str2)
