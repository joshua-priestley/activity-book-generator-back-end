from flask import Flask, session
from flask_session import Session
import redis

def create_app(test_config=None):
  """Application factory"""
  app = Flask(__name__)
 
  # Use test config if supplied
  if test_config:
    app.config.from_mapping(test_config)
  
  app.config["SESSION_TYPE"]  = "redis"
  app.config["SESSION_REDIS"] = redis.from_url('redis://db:6379')
  app.config['SECRET_KEY'] = 'super secret key'   

  sess = Session()
  sess.init_app(app)

  # Register blueprints
  from . import root, anagrams
  app.register_blueprint(root.bp)
  app.register_blueprint(anagrams.bp)

  return app
