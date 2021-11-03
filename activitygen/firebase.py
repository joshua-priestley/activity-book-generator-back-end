import firebase_admin
from firebase_admin import auth, credentials
from flask import Flask, request
from functools import wraps

# Add a folder called key and file containing the admin sdk key
cred = credentials.Certificate("../keys/themed-activity-book-firebase-adminsdk.json")

app = firebase_admin.initialize_app(cred)

def check_token(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if not request.headers.get('authorization'):
            return {'message': 'No token provided'},400
        try:
            user = auth.verify_id_token(request.headers['authorization'])
            request.user = user
        except:
            return {'message':'Invalid token provided.'},400
        return f(*args, **kwargs)
    return wrap
