import cairosvg
import httpx
import io
import numpy as np
from flask import current_app
from typing import List, Tuple
from PIL import Image, ImageFilter

from .noun_project_adapter import get_icons

REDIS_KEY_PREFIX = "noun.project.icons"
DEFAULT_ICON_WIDTH, DEFAULT_ICON_HEIGHT = 512, 512

def silhouette_pixel_art(image_bytes: bytes, dimensions: Tuple[int, int]):
  with Image.open(io.BytesIO(image_bytes)) as image:
    # Edge enhance
    edge_enhanced = image.filter(ImageFilter.EDGE_ENHANCE_MORE)

    # Make black & white
    silhouette = Image.new("RGBA", edge_enhanced.size, "WHITE")
    silhouette.paste(edge_enhanced, (0, 0), edge_enhanced)
    silhouette = silhouette.convert("1")

    # Trim surrounding whitespace
    silhouette_arr = np.asarray(silhouette)
    min_row = 0
    while np.all(silhouette_arr[min_row]):
      min_row += 1
    min_col = 0
    while np.all(silhouette_arr[:, min_col]):
      min_col += 1
    max_row = silhouette_arr.shape[0] - 1
    while np.all(silhouette_arr[max_row]):
      max_row -= 1
    max_col = silhouette_arr.shape[1] - 1
    while np.all(silhouette_arr[:, max_col]):
      max_col -= 1
    start = min(min_row, min_col)
    end = max(max_row, max_col)
    silhouette = silhouette.crop((start, start, end, end))

    # Resize, pixelate
    silhouette.thumbnail(dimensions)
    return np.asarray(silhouette)

def get_icon_pngs(term: str) -> List[bytes]:
  term = term.lower()
  redis = current_app.config["REDIS_CONN"]
  redis_key = f"{REDIS_KEY_PREFIX}:{term}"
  
  # Attempt to fetch from cache
  icon_pngs = list(redis.smembers(redis_key))

  if not icon_pngs:
    # Cache miss, fetch from API
    try:
      res = get_icons(term, limit_to_public_domain=1, limit=50)
    except httpx.HTTPStatusError:
      return []

    for icon in res["icons"]:
      try:
        icon_png = cairosvg.svg2png(url=icon["icon_url"],
                                    output_width=DEFAULT_ICON_WIDTH,
                                    output_height=DEFAULT_ICON_HEIGHT)
        icon_pngs.append(icon_png)
      except Exception:
        pass

    # Add new icons to cache
    if icon_pngs:
      redis.sadd(redis_key, *icon_pngs)
  
  return icon_pngs
