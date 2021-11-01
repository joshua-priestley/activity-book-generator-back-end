from pymongo import MongoClient

client = MongoClient('mongodb://mongo:27017')

db = client.activity_book_gen

users = db.users
books = db.books
