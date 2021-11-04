from flask import Blueprint, jsonify, make_response, request, session
import random
#from werkzeug.wrappers import request

from . import anagrams
from . import maze
from . import word_search
from . import fill_in_the_blanks
from .themes import themes
from .firebase import check_token

bp = Blueprint("root", __name__)

@bp.route("/")
def root():
  return jsonify("Activity Book Generator back-end is running")

@bp.route("/puzzles")
def puzzles():
  return jsonify(["Word Search", "Anagrams"])

@bp.route("/whoami")
@check_token
def whoami():
  return jsonify({"user" : str(request.user["email"]) })

#@bp.route("/word-search")
#def word_search_endpoint():
#  words = ["squirrel", "wolf", "bear", "lion", "tiger", "tortoise"]
#  hidden_message = "We love animals"
#  (cells, hangman_words, _) = word_search.generate(words, hidden_message)
#  data = {
#    "cells": cells,
#    "hangman_words": hangman_words,
#    "words": words,
#  }
#  options = {
#    "encoding": "UTF-8",
#    "page-size": "A4",
#    "dpi": 400,
#    "disable-smart-shrinking": "",
#    "margin-top": "1in",
#    "margin-right": "1in",
#    "margin-bottom": "1in",
#    "margin-left": "1in"
#  }
#  pdf = pdfkit.from_string(word_search.generate_html(data), False, options=options, css="style/styles.css")
#  response = make_response(pdf)
#  response.headers['Content-Type'] = 'application/pdf'
#  response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
#  return response


@bp.route("/themes", methods = ['GET', 'POST'])
def themesEndpoint():
  if request.method == 'GET':
    result = themes.copy()

    if "custom themes" in session:
      result = { **result, **session["custom themes"] }

    return jsonify(result)

  res = request.json

  if "custom themes" not in session:
    session["custom themes"] = {}

  session["custom themes"][res["theme"]] = res["words"]

  return jsonify("Added theme")

activity_map = {
  'anagrams': anagrams.generate_data,
  'word-search': word_search.generate,
  'fill-in-the-blanks': fill_in_the_blanks.generate,
  'maze': maze.generate_maze
}

html_gen_map = {
  "anagrams": anagrams.generate_html,
  "word-search": word_search.generate_html,
  "fill-in-the-blanks": fill_in_the_blanks.generate_html,
  "maze": maze.generate_html
}

# {
# "theme": "christmas",
# "anagrams": 3,
# "wordsearch": 4
# } 
#@bp.route("/generate", methods=["post"])
#def generate():
#  body = request.json
# 
#  userThemes = themes.copy()
#
#  if "custom themes" in session:
#    userThemes = { **userThemes, **session["custom themes"] }
#
#
#  wordset = userThemes[body["theme"]]
#  numWords = len(wordset)
#
#  json = []
#  for _ in range(body["Anagrams"]):
#    # select random words for anagram
#    puzzleWords = random.sample(wordset, min(numWords, 10))
#    json.append({"activity": "anagrams", "inputs": {
#      "theme": body["theme"],
#      "words": puzzleWords,
#      "difficulty": anagrams.Difficulty.HARD
#    }})
#    
#  for n in range(body["Word Search"]):
#    l = [w for w in wordset if " " not in w]
#    puzzleWords = random.sample(l, min(len(l), 6))
#    json.append({"activity": "word-search", "inputs": {
#      "hidden_message": puzzleWords.pop(),
#      "words": puzzleWords
#    }})
#
#  for n in range(body["Maze"]):
#    json.append({
#    "activity": "maze", 
#    "inputs": {
#      "grid_width": 15,
#      "grid_height": 15
#    }, 
#    "html_data": {
#      "title": "maze",
#      "instructions": "Complete the maze"}
#    })
#  #   maze = Maze(15,15,0,0)
#  #   maze.make_maze()
#  #   maze.generate_svg()
#
#  
#  for _ in range(body["Fill In the Blanks"]):
#    puzzleWords = random.sample(wordset, min(numWords, 10))
#    json.append({"activity": "fill-in-the-blanks", "inputs": {
#      "theme": body["theme"],
#      "words": puzzleWords,
#      "difficulty": anagrams.Difficulty.HARD
#    }})
#  
#  random.shuffle(json)
#
#  pdf_result = pdf(json)
#  response = make_response(pdf_result)
#  response.headers['Content-Type'] = 'application/pdf'
#  response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
#  return response

#def pdf(activities):
#  html = []
#  for activity in activities:
#    # Generate activity internal representation
#    data = activity_map[activity["activity"]](**activity["inputs"])
#
#    data = process(data, activity)
#
#    # Generate HTML and append to output
#    if "html_data" in activity:
#      html.append(html_gen_map[activity["activity"]](data, activity["html_data"]))
#    else:  
#      html.append(html_gen_map[activity["activity"]](data))
#    
#    
#  return pdfkit.from_string("".join(html), False, css="style/styles.css", options={
#    "encoding": "UTF-8",
#    "page-size": "A4",
#    "dpi": 400,
#    "disable-smart-shrinking": "",
#    "margin-top": "1in",
#    "margin-right": "1in",
#    "margin-bottom": "1in",
#    "margin-left": "1in"
#  })

def process(data, activity):
  if activity["activity"] == "word-search":
    cells, hangman_words, _ = data
    data = {
      "cells": cells,
      "hangman_words": hangman_words,
      "words": activity["inputs"]["words"]
    }


  return data
