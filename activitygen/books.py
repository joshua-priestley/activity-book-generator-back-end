from flask import Blueprint, request, make_response, jsonify
from . import mongo
from bson.objectid import ObjectId
from .firebase import check_token

bp = Blueprint("books", __name__)

@bp.route("/books", methods=['GET', 'POST','DELETE', 'PATCH'])
@check_token
def books():
  
  userId = request.userId

  if request.method == 'GET':
    user = mongo.users.find_one({ '_id' : ObjectId(userId) })

    res = list(user['books'])

    for i in range(len(res)):
      res[i]['book_id'] = str(res[i]['book_id'])

    return make_response(jsonify(res), 200)

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
@check_token
def content():

  userId = request.userId
  book_id = request.args.get('book_id')

  if request.method == 'GET':
    book = mongo.books.find_one({ '_id': ObjectId(book_id), 'parent' : ObjectId(userId) })

    return make_response(jsonify(book['components']), 200)

  elif request.method == 'PATCH':

    components = request.get_json()
    
    result = mongo.books.update_one({ '_id': ObjectId(book_id), 'parent' : ObjectId(userId) }, { '$set' : { 'components' : components } })

    return make_response(jsonify({ "updated" : result.modified_count }), 200)
  
