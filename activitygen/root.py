import re
from flask import Blueprint, jsonify, make_response, request
from flask.templating import render_template
from werkzeug.utils import send_file
import pdfkit
#from werkzeug.wrappers import request

from . import activities

bp = Blueprint("root", __name__)

@bp.route("/")
def root():
  return jsonify("Activity Book Generator back-end is running")


activity_map = {
  'anagram': activities.generate_anagrams,
  'word-search': activities.generate_word_search
}

# Example json:
#
#   {
#     "0": {"puzzle": "anagram", "data": ["test", "hello", "world"]}, 
#     "1": {"puzzle": "anagram", "data": ["christmas", "presents"]}
#   }

@bp.route("/pdf/", methods=["post"])
def pdf():

  activity = request.get_json() 

  html = ""
  for key in activity:
    print(activity[key])
    html += " ".join(activity_map[activity[key]['puzzle']](activity[key]['data'], activities.Difficulty.HARD))
    html += " "


  print("html: " + html)
  pdf = pdfkit.from_string(html, False)

  response = make_response(pdf)
  response.headers['Content-Type'] = 'application/pdf'
  response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
  return response



