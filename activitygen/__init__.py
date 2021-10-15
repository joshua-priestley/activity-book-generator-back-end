from flask import Flask

def create_app(test_config=None):
  """Application factory"""
  app = Flask(__name__)

  # Use test config if supplied
  if test_config:
    app.config.from_mapping(test_config)

  return app
 