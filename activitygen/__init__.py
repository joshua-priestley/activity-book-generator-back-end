from flask import Flask, session
from flask_session import Session
from flask_cors import CORS
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
  #app.config['CORS_ORIGINS'] = 'http://localhost:3000,http://cloud-vm-43-12.doc.ic.ac.uk,http://cloud-vm-43-12.doc.ic.ac.uk:80,http://cloud-vm-43-12.doc.ic.ac.uk:8080'

  sess = Session()
  sess.init_app(app)

  CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://cloud-vm-43-12.doc.ic.ac.uk", "http://cloud-vm-43-12.doc.ic.ac.uk:80", "http://cloud-vm-43-12.doc.ic.ac.uk:8080"]}})

  # Register blueprints
  from . import root, anagrams
  app.register_blueprint(root.bp)
  app.register_blueprint(anagrams.bp)

  return app
