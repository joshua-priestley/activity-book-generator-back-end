import re
from flask import Blueprint, jsonify, make_response
from flask.templating import render_template
from werkzeug.utils import send_file
import pdfkit

bp = Blueprint("root", __name__)

@bp.route("/")
def root():
  return jsonify("Activity Book Generator back-end is running")


@bp.route("/pdf/")
def pdf():
  pdf = pdfkit.from_string("Test", False)

  response = make_response(pdf)
  response.headers['Content-Type'] = 'application/pdf'
  response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
  return response