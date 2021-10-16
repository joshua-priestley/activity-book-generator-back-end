import re
from flask import Blueprint, jsonify

bp = Blueprint("root", __name__)

@bp.route("/")
def root():
  return jsonify("Activity Book Generator back-end is running")

# @bp.route("/pdf/")
# def root():
#   return {"pdf": "Pdf goes here"}

@bp.route("/pdf/")
def pdf():
  return jsonify("Activity Book Generator back-end is running")