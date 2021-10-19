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
  'anagram': activities.generate_anagrams
}


# Will eventually be post only
@bp.route("/pdf/", methods=["post"])
def pdf():
  # Hard coded post for now
  activity = request.get_json() #[{"id": "anagram", "num": "5"}]

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




  # url = "file"
    # # Generate UUID for each file uploaded
    # tex_uuid = uuid.uuid4()
    # tex_filename = 'tex/{}'.format(str(tex_uuid))
    # tex_url = url[:-3] + 'tex'
    # urllib.response.urlretrieve(tex_url, tex_filename)

    # # Try to render LaTeX to PDF
    # tex_render = pexpect.spawn("pdflatex -interaction=nonstopmode -output-directory=tex {}".format("file"))
    # try:
    #     tex_render.expect("Output written on", timeout=30)
    # except pexpect.TIMEOUT:
    #     return "Timeout when rendering the PDF!"

    # # Load PDF into memory
    # pdf_filename = tex_filename + '.pdf'
    # pdf_file = open(pdf_filename)

    # # Remove files from filesystem
    # os.remove(tex_filename)
    # os.remove(pdf_filename)
    # os.remove(tex_filename+'.aux')
    # os.remove(tex_filename+'.log')

   # return Response(pdf_file, mimetype='application/pdf')