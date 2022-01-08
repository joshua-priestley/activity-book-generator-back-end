import numpy as np
import random
from flask import abort, Blueprint, request
from typing import Dict

from .commons.icons import get_icon_pngs, silhouette_pixel_art

bp = Blueprint("nonogram", __name__, url_prefix="/activities/nonogram")

@bp.route("/state")
def get_state():
  """Returns internal nonogram state from provided options"""
  theme = request.args.get("theme")
  width = int(request.args.get("width", 15))
  height = int(request.args.get("height", width))

  images = get_icon_pngs(theme)
  if not images:
    abort(404, f"No suitable images found for theme '{theme}'")
  image_bytes = random.choice(images)
  image = silhouette_pixel_art(image_bytes, (width, height))
  return generate_nonogram(image)

def generate_nonogram(image) -> Dict:
  row_numbers, column_numbers = ([
    [group.size for group in np.split(span, np.where(np.diff(span))[0] + 1) if not group[0]]
    for span in img]
    for img in (image, image.T))

  # Replace empty numbers lists with single 0
  row_numbers, column_numbers = ([groups if groups else [0] for groups in numbers]
    for numbers in (row_numbers, column_numbers))

  return {
    "description": ("Some of the squares in the grid below should be shaded in. "
                  "Beside each row and column, you are given the lengths of groups of squares to fill in.\n"
                  "For example, the numbers \"2 3\" mean there should be sets of 2 and 3 consecutive shaded "
                  "cells in that row or column.\n"
                  "Shade in all the correct cells to reveal a themed picture!"),
    "image": image.tolist(),
    "row_numbers": row_numbers,
    "column_numbers": column_numbers
  }
