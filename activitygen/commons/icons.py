import cairosvg
import httpx
from flask import current_app
from typing import List

from .noun_project_adapter import get_icons

REDIS_KEY_PREFIX = "noun.project.icons"
DEFAULT_ICON_WIDTH, DEFAULT_ICON_HEIGHT = 512, 512

def get_icon_pngs(term: str) -> List[bytes]:
  term = term.lower()
  redis = current_app.config["SESSION_REDIS"]
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
