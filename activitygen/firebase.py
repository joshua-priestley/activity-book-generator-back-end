import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("../keys/themed-activity-book-firebase-adminsdk.json")
firebase_admin.initialize_app(cred)