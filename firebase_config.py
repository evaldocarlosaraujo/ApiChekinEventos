import firebase_admin
from firebase_admin import credentials, db

def initialize_firebase():
    cred = credentials.Certificate("apicheckin-8399e-firebase-adminsdk-fbsvc-317c368f37.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://apicheckin-8399e-default-rtdb.firebaseio.com/'
    })