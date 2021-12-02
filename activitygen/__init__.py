from flask import Flask
from flask_cors import CORS
import os

def create_app(test_config=None):
  """Application factory"""
  app = Flask(__name__)
  print(__name__)
 
  # Use test config if supplied
  if test_config:
    app.config.from_mapping(test_config)

  origins = ["http://localhost:3000"]
  if "FRONT_END_URL" in os.environ:
    origins.append(os.environ["FRONT_END_URL"])

  CORS(app, origins = origins, supports_credentials=True)

  # Register blueprints
  from . import root, anagrams, fill_in_the_blanks, maze, sudoku, word_search, books, image_shuffle, nonogram
  app.register_blueprint(root.bp)
  app.register_blueprint(anagrams.bp)
  app.register_blueprint(fill_in_the_blanks.bp)
  app.register_blueprint(maze.bp)
  app.register_blueprint(nonogram.bp)
  app.register_blueprint(sudoku.bp)
  app.register_blueprint(word_search.bp)
  app.register_blueprint(books.bp)
  app.register_blueprint(image_shuffle.bp)

  return app
