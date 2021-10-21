from flask import Blueprint, jsonify, make_response
import pdfkit
#from werkzeug.wrappers import request

from . import anagrams

bp = Blueprint("root", __name__)

@bp.route("/")
def root():
  return jsonify("Activity Book Generator back-end is running")

html_gen_map = {
  "anagrams": anagrams.generate_html
}

# Example json:
#
#   {
#     "0": {"puzzle": "anagram", "data": ["test", "hello", "world"]}, 
#     "1": {"puzzle": "anagram", "data": ["christmas", "presents"]}
#   }

@bp.route("/pdf/")
def pdf():

  # Example data for now – TODO delete and replace with data fetched from database
  data = [
    {
      "activity": "anagrams",
      "data": {
        "theme": "Christmas",
        "words": ["christmas tree", "santa", "reindeer", "present", "elf", "bauble", "frosty the snowman", "sleigh", "stocking"],
        "anagrams": ["amcistshr eert", "aants", "rnerdeei", "ertpens", "lfe", "bbueal", "royfts teh nmanosw", "egislh", "igkcnsot"]
      }
    },
    {
      "activity": "anagrams",
      "data": {
        "theme": "animal",
        "words": ["cow", "sheep", "cheetah", "mouse", "aardvark", "elephant", "monkey", "rabbit", "mountain lion", "hippopotamus"],
        "anagrams": ["owc", "eshep", "aeehhtc", "eomus", "rvaakdra", "eltnhpae", "nemoky", "biatbr", "niouatnm ilno", "ptiposauohpm"]
      }
    }
  ]

  html = (html_gen_map[activity["activity"]](activity["data"]) for activity in data)

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
