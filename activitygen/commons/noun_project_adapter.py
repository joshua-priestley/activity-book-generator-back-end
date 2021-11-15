import httpx
import os
from authlib.integrations.httpx_client import OAuth1Auth
from typing import Dict

os.environ["AUTHLIB_INSECURE_TRANSPORT"] = "1"
NOUN_PROJECT_API_KEY = os.getenv("NOUN_PROJECT_API_KEY", "")
NOUN_PROJECT_API_SECRET = os.getenv("NOUN_PROJECT_API_SECRET", "")

auth = OAuth1Auth(
  client_id=NOUN_PROJECT_API_KEY,
  client_secret=NOUN_PROJECT_API_SECRET
)

def noun_project_client():
  if not NOUN_PROJECT_API_KEY or not NOUN_PROJECT_API_SECRET:
    raise RuntimeError("Missing Noun Project authentication environment variable(s)")
  return httpx.Client(base_url="http://api.thenounproject.com", auth=auth)

def get_icons(term: str,
              limit_to_public_domain: int = None,
              limit: int = None,
              offset: int = None,
              page: int = None) -> Dict:
  params = {k: v for k, v in {
    "limit_to_public_domain": limit_to_public_domain,
    "limit": limit,
    "offset": offset,
    "page": page
  }.items() if v is not None}

  with noun_project_client() as client:
    res = client.get(f"/icons/{term}", params=params)
  res.raise_for_status()
  return res.json()
