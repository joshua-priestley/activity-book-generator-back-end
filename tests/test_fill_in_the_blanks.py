import pytest
from activitygen.commons.difficulty import Difficulty
from activitygen.fill_in_the_blanks import blank_word, generate, generate_html

SAMPLE_WORDS = ["cow", "reindeer", "skeleton", "princess", "christmas tree", "a", "tv"]

@pytest.mark.parametrize("difficulty", (Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD))
def test_letters_not_rearranged(difficulty):
  """Letters should only be blanked out, not rearranged"""
  blanked_words = map(lambda word: blank_word(word, difficulty), SAMPLE_WORDS)

  for word, blanked_word in zip(SAMPLE_WORDS, blanked_words):
    assert len(word) == len(blanked_word)

    for word_char, blanked_word_char in zip(word, blanked_word):
      assert word_char == blanked_word_char or blanked_word_char == "_"

@pytest.mark.parametrize("difficulty", (Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD))
def test_at_least_one_letter_blanked(difficulty):
  """There should be at least one blanked out character"""
  blanked_words = map(lambda word: blank_word(word, difficulty), SAMPLE_WORDS)
  assert all("_" in blanked_word for blanked_word in blanked_words)

@pytest.mark.parametrize("difficulty", (Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD))
def test_at_least_one_letter_not_blanked(difficulty):
  """For words longer than one character, at least one character should remain unblanked"""
  words = ["me", "cat", "mage", "heart", "flower", "banquet", "darkness", "enchanted"]
  blanked_words = map(lambda word: blank_word(word, difficulty), words)
  assert all(any(char.isalpha() for char in blanked_word)
             for blanked_word in blanked_words)

@pytest.mark.parametrize("difficulty", (Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD))
def only_letters_are_blanked(difficulty):
  """Only letters should be blanked out, not spaces, hyphens or apostrophes"""
  xmas_word, jacko_word = "christmas tree", "jack-o'-lantern"
  blanked_xmas_word, blanked_jacko_word = blank_word(xmas_word, difficulty), blank_word(jacko_word, difficulty)

  assert blanked_xmas_word[9] == " "

  assert blanked_jacko_word[4] == "-"
  assert blanked_jacko_word[6:8] == "'-"

@pytest.mark.parametrize("difficulty", (Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD))
def test_data_contains_theme_and_original_words(difficulty):
  """Fill In the Blanks internal data representation should remember theme and original words"""
  sample_theme = "Christmas"
  data = generate(sample_theme, SAMPLE_WORDS, difficulty)
  assert "theme" in data and data["theme"] == sample_theme
  assert "words" in data and data["words"] == SAMPLE_WORDS

def test_html_contains_all_blanked_words(app):
  """Generated HTML should contain every blanked word from the internal data representation"""
  with app.test_request_context():
    SAMPLE_DATA = {
      "theme": "Christmas",
      "words": ["christmas tree", "santa", "reindeer", "present", "elf", "bauble", "sleigh", "stocking"],
      "blanked_words": ["chri___a_ t_ee", "s__ta", "_ein_ee_", "pres_n_", "el_", "_aubl_", "_leig_", "s_oc_ing"]
    }
    html = generate_html(SAMPLE_DATA)
    assert all(blanked_word in html for blanked_word in SAMPLE_DATA["blanked_words"])
  