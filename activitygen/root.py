from flask import Blueprint, jsonify, make_response, request, session
import pdfkit
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
  'anagrams': anagrams.generate_data,
  'word-search': word_search.generate
}

html_gen_map = {
  "anagrams": anagrams.generate_html
}

# Example json:
#
#   {
#     "0": {"puzzle": "anagram", "data": ["test", "hello", "world"]}, 
#     "1": {"puzzle": "anagram", "data": ["christmas", "presents"]}
#   }

@bp.route("/pdf/", methods=["post"])
def pdf():
  # Example data
  activities = [
    {
      "activity": "anagrams",
      "inputs": {
        "theme": "cities",
        "words": ["new york", "paris", "hong kong", "amsterdam", "tokyo", "london", "singapore", "chicago"],
        "difficulty": anagrams.Difficulty.HARD
      }
    },
    # {
    #   "activity": "word search",
    #   "inputs": {
    #     "words": ["london", ...],
    #     "hidden_message": "skyscrapers are cool"
    #   }
    # }
  ]
  pdf = generate_pdf(activities)
  response = make_response(pdf)
  response.headers['Content-Type'] = 'application/pdf'
  response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
  return response

def generate_pdf(activities):
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
