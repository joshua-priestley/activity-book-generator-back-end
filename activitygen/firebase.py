import firebase_admin
from firebase_admin import auth, credentials
from flask import Flask, request
from functools import wraps
from . import mongo

# Add a folder called key and file containing the admin sdk key
cred = credentials.Certificate("keys/themed-activity-book-firebase-adminsdk.json")

app = firebase_admin.initialize_app(cred)

def check_token(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if not request.headers.get('authorization'):
            return {'message': 'No token provided'},400
        try:
            user = auth.verify_id_token(request.headers['authorization'])
            request.user = user

            dbUser = mongo.users.find_one({ 'firebaseId' : user['user_id'] })

            if dbUser is None:
              newUser = { 'firebaseId' : user['user_id'], 'books' : [] }
              dbUser = mongo.users.insert_one(newUser)
            
            request.userId = dbUser['_id']
        except:
            return {'message':'Invalid token provided.'},400
        return f(*args, **kwargs)
    return wrap
