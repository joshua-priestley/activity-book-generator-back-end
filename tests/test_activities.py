import pytest
from activitygen.activities import Difficulty, generate_anagrams, generate_data, generate_html
from collections import Counter

SAMPLE_WORDS = ["cow", "reindeer", "skeleton", "princess", "christmas tree", "a", "tv"]

@pytest.mark.parametrize("difficulty", (Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD))
def test_anagram_for_each_word(difficulty):
  """Number of anagrams should equal number of words given"""
  assert len(SAMPLE_WORDS) == len(generate_anagrams(SAMPLE_WORDS, difficulty))

@pytest.mark.parametrize("difficulty", (Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD))
def test_anagram_gen_gives_rearrangement(difficulty):
  """Anagrams should use exactly the same characters as the original strings"""
  assert all(is_rearrangement(word, anagram)
             for word, anagram in zip(SAMPLE_WORDS, generate_anagrams(SAMPLE_WORDS, difficulty)))

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

@pytest.mark.parametrize("difficulty", (Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD))
def test_anagram_data_contains_theme_and_original_words(difficulty):
  """Anagram internal data representation should remember theme and original words"""
  sample_theme = "Christmas"
  data = generate_data(sample_theme, SAMPLE_WORDS, difficulty)
  assert "theme" in data and data["theme"] == sample_theme
  assert "words" in data and data["words"] == SAMPLE_WORDS

def test_anagram_html_contains_all_anagrams(app):
  with app.test_request_context():
    SAMPLE_DATA = {
      "theme": "Christmas",
      "words": ["christmas tree", "santa", "reindeer", "present", "elf", "bauble", "frosty the snowman", "sleigh", "stocking"],
      "anagrams": ["amcistshr eert", "aants", "rnerdeei", "ertpens", "lfe", "bbueal", "royfts teh nmanosw", "egislh", "igkcnsot"]
    }
    html = generate_html(SAMPLE_DATA)
    assert all(anagram in html for anagram in SAMPLE_DATA["anagrams"])

def is_rearrangement(str1: str, str2: str) -> bool:
  return Counter(str1) == Counter(str2)
