from flask import Blueprint, request, session, make_response, jsonify
from . import mongo
from bson.objectid import ObjectId

bp = Blueprint("books", __name__)

@bp.route("/books", methods=['GET', 'POST','DELETE', 'PATCH'])
def books():
  if 'userId' not in session:
    data = { 'invalid' : 'not logged in' }
    return make_response(jsonify(data), 400)

  userId = session['userId']

  if request.method == 'GET':
    user = mongo.users.find_one({ '_id' : ObjectId(userId) })

    return make_response(str(user['books']), 200)

  elif request.method == 'POST':

    title = request.args.get('title')

    book = mongo.books.insert_one({ 'parent' : ObjectId(userId), 'components' : [] })

    new_book = { 'book_id' : book.inserted_id, 'title' : title }

    mongo.users.update_one({ '_id' : ObjectId(userId) }, {'$push': {'books': new_book}})
    user = mongo.users.find_one()

    return make_response(jsonify({'book_id' : str(book.inserted_id)}), 200)

  elif request.method == 'DELETE':

    book_id = request.args.get('book_id')

    result = mongo.users.update_one({ '_id' : ObjectId(userId) },
      { '$pull': { 'books': { 'book_id': ObjectId(book_id) } } })

    if result.modified_count == 1:
      mongo.books.delete_one({ '_id': ObjectId(book_id), 'parent' : ObjectId(userId) })

    return make_response(jsonify({ 'deleted' : result.modified_count }), 200)

  elif request.method == 'PATCH':

    title = request.args.get('title')
    book_id = request.args.get('book_id')

    mongo.users.update_one({ '_id' : ObjectId(userId), 'books.book_id' : ObjectId(book_id) }, { '$set' : { 'books.$.title' : title } })

    return make_response(jsonify({'updated book' : book_id}), 200)

@bp.route("/content", methods=["GET", "PATCH"])
def content():
  if 'userId' not in session:
    data = { 'invalid' : 'not logged in' }
    return make_response(jsonify(data), 400)

  userId = session['userId']
  book_id = request.args.get('book_id')

  if request.method == 'GET':
    book = mongo.books.find_one({ '_id': ObjectId(book_id), 'parent' : ObjectId(userId) })

    return make_response(jsonify(book['components']), 200)

  elif request.method == 'PATCH':

    components = request.get_json()
    
    result = mongo.books.update_one({ '_id': ObjectId(book_id), 'parent' : ObjectId(userId) }, { '$set' : { 'components' : components } })

    return make_response(jsonify({ "updated" : result.modified_count }), 200)
  