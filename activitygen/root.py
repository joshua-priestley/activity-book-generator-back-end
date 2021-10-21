from flask import Blueprint, jsonify, make_response, request, session
import pdfkit
import random
#from werkzeug.wrappers import request

from . import anagrams
from . import word_search
from .themes import themes

bp = Blueprint("root", __name__)

@bp.route("/")
def root():
  return jsonify("Activity Book Generator back-end is running")

@bp.route("/themes", methods = ['GET', 'POST'])
def themesEndpoint():
  if request.method == 'GET':
    result = themes.copy()

    if "custom themes" in session:
      result = result | session["custom themes"]

    return jsonify(result)

  res = request.json

  if "custom themes" not in session:
    session["custom themes"] = {}

  session["custom themes"][res["theme"]] = res["words"]

  return jsonify("Added theme")

activity_map = {
  'anagram': anagrams.generate_anagrams,
  'word-search': word_search.generate
}


# {
# "theme": "christmas",
# "anagrams": 3,
# "wordsearch": 4
# } 
@bp.route("/generate", methods=["post"])
def generate():
  body = request.json

  wordset = themes[body["theme"]]
  numWords = len(wordset)

  json = {"activities" : []}
  for _ in range(body["anagrams"]):
    # select random words for anagram
    puzzleWords = random.sample(wordset, min(numWords, 5))
    anagramData = anagrams.generate_data(body["theme"], puzzleWords, anagrams.Difficulty.HARD)
    json["activities"].append({"activity": "anagrams", "inputs" : anagramData})
    
  for n in range(body["wordsearch"]):
    puzzleWords = random.sample(wordset, min(numWords, 5))
    

  return pdf(json)

@bp.route("/pdf/")
def pdf(json):

  data = json["activities"]
  # Example data for now – TODO delete and replace with data fetched from database
  # data = [
  #   {
  #     "activity": "anagrams",
  #     "data": {
  #       "theme": "Christmas",
  #       "words": ["christmas tree", "santa", "reindeer", "present", "elf", "bauble", "frosty the snowman", "sleigh", "stocking"],
  #       "anagrams": ["amcistshr eert", "aants", "rnerdeei", "ertpens", "lfe", "bbueal", "royfts teh nmanosw", "egislh", "igkcnsot"]
  #     }
  #   },
  #   {
  #     "activity": "anagrams",
  #     "data": {
  #       "theme": "animal",
  #       "words": ["cow", "sheep", "cheetah", "mouse", "aardvark", "elephant", "monkey", "rabbit", "mountain lion", "hippopotamus"],
  #       "anagrams": ["owc", "eshep", "aeehhtc", "eomus", "rvaakdra", "eltnhpae", "nemoky", "biatbr", "niouatnm ilno", "ptiposauohpm"]
  #     }
  #   }
  # ]

  html_gen_map = {
    "anagrams": anagrams.generate_html
  }

  html = (html_gen_map[activity["activity"]](activity["inputs"]) for activity in data)

  pdf = pdfkit.from_string("".join(html), False, options={
    "encoding": "UTF-8",
    "page-size": "A4",
    "dpi": 400,
    "disable-smart-shrinking": "",
    "margin-top": "1in",
    "margin-right": "1in",
    "margin-bottom": "1in",
    "margin-left": "1in"
  })

  response = make_response(pdf)
  response.headers['Content-Type'] = 'application/pdf'
  response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
  return response
