from flask import Blueprint, session, request, make_response, jsonify
from . import mongo

bp = Blueprint("login", __name__)

@bp.route("/login", methods=['GET'])
def login():
  username = request.args.get('username')
  user     = mongo.users.find_one({ 'username' : username })

  if user is None:
    user   = { 'username' : username, 'books' : [] }
    result = mongo.users.insert_one(user)
    userId = result.inserted_id
  else:
    userId = user['_id']

  session['userId'] = userId

  data = { 'id': str(userId) }
  return make_response(jsonify(data), 200)

@bp.route("/logout", methods=['GET'])
def logout():
  if 'userId' in session:  
    data = { 'id': str(session['userId']) }
    session.pop('userId')
    return make_response(jsonify(data), 200)

  data = { 'invalid' : 'not logged in' }
  return make_response(jsonify(data), 400)
