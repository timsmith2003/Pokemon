# admin.py

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
from google.cloud.firestore_v1 import FieldFilter, Or
import authentication


db = authentication.db.collection('pokemon')

with open('pokedex.json') as data_file:    
    data = json.load(data_file)
    for v in data:
        doc_ref = db.document(str(v["id"]))
        doc_ref.set(v)

# This code brings data back in
# doc_ref = db.collection("pokemon").document("Poison")
# doc = doc_ref.get()
# print(doc.to_dict())

# docs = (
#     db.collection("pokemon")
#     .where(filter=FieldFilter("id", "==", True))
#     .stream()
# )
#
# for d in docs:
#     print(f"{d.id} => {d.to_dict()}")


# docs = db.collection("pokemon").stream()
#
# for doc in docs:
#     print(f"{doc.id} => {doc.to_dict()}")

# pokemon_ref = db.collection("pokemon")
# pokemon_ref.where(filter = FieldFilter("name", "==", "Charmander"))
# pokemon_ref.where(filter = FieldFilter("type", "==", "Fire"))
# pokemon_docs = pokemon_ref.stream()
# for doc in pokemon_docs:
#     print(f"{doc.id} => {doc.to_dict()}")


# query = pokemon_ref.where(
#     filter=Or(
#         [
#             FieldFilter("name", "==", "Charmander"),
#             FieldFilter("type", "==", ["Fire", "Flying"]),
#         ]
#     )
# )
# docs = query.stream()
# for doc in docs:
#     print(f"{doc.id} => {doc.to_dict()}")

# query = pokemon_ref.where(
#     filter=FieldFilter("type", "array_contains", "poison"))
#     .stream()
# doc = query.get()
# print(doc.to_dict())

#Flatten the data so thweres not sublists in the attributes part


