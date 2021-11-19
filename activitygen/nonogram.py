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

  return {
    "image": image.tolist(),
    "row_numbers": row_numbers,
    "column_numbers": column_numbers
  }