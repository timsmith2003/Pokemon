import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("pokemon-18f65-firebase-adminsdk-fbsvc-b7381bea5e.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
