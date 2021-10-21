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

@bp.route("/word-search")
def word_search_endpoint():
  words = ["squirrel", "wolf", "bear", "lion", "tiger", "tortoise"]
  hidden_message = "We love animals"
  (cells, hangman_words, _) = word_search.generate(words, hidden_message)
  data = {
    "cells": cells,
    "hangman_words": hangman_words,
    "words": words,
  }
  options = {
    "encoding": "UTF-8",
    "page-size": "A4",
    "dpi": 400,
    "disable-smart-shrinking": "",
    "margin-top": "1in",
    "margin-right": "1in",
    "margin-bottom": "1in",
    "margin-left": "1in"
  }
  pdf = pdfkit.from_string(word_search.generate_html(data), False, options=options)
  response = make_response(pdf)
  response.headers['Content-Type'] = 'application/pdf'
  response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
  return response


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
  'anagrams': anagrams.generate_data,
  'word-search': word_search.generate
}

html_gen_map = {
  "anagrams": anagrams.generate_html,
  "word-search": word_search.generate_html
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

  json = []
  for _ in range(body["anagrams"]):
    # select random words for anagram
    puzzleWords = random.sample(wordset, min(numWords, 5))
    json.append({"activity": "anagrams", "inputs" : {
      "theme": body["theme"],
      "words": puzzleWords,
      "difficulty": anagrams.Difficulty.HARD
    }})
    
  for n in range(body["wordsearch"]):
    puzzleWords = random.sample(wordset, min(numWords, 5))

  pdf_result = pdf(json)
  response = make_response(pdf_result)
  response.headers['Content-Type'] = 'application/pdf'
  response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
  return response

def pdf(activities):
  html = []
  for activity in activities:
    # Generate activity internal representation
    data = activity_map[activity["activity"]](**activity["inputs"])

    # Generate HTML and append to output
    html.append(html_gen_map[activity["activity"]](data))

  return pdfkit.from_string("".join(html), False, options={
    "encoding": "UTF-8",
    "page-size": "A4",
    "dpi": 400,
    "disable-smart-shrinking": "",
    "margin-top": "1in",
    "margin-right": "1in",
    "margin-bottom": "1in",
    "margin-left": "1in"
  })
