import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

cred = credentials.Certificate("pokemon-18f65-firebase-adminsdk-fbsvc-b7381bea5e.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

with open('pokedex.json') as data_file:    
    data = json.load(data_file)
    for v in data:
        doc_ref = db.collection("pokemon").document(str(v["id"]))
        doc_ref.set(v)

#This code brings data back in
doc_ref = db.collection("pokemon").document("1")
doc = doc_ref.get()
print(doc.to_dict())

#Flatten the data so thweres not sublists in the attributes part


