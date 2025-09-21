from google.cloud.firestore_v1.base_query import FieldFilter
import json
import authentication
from poke_class import Pokemon

db = authentication.db.collection("pokemon")

with open('pokedex.json') as data_file:    
    data = json.load(data_file)
    for v in data:
        doc_ref = db.document(str(v["id"]))
        doc_ref.set(v)



query = db.where(
    filter=FieldFilter("hp", ">", 100)
).where("hp", "<", 150).get()

for doc in query:
    p = Pokemon.from_dict(source=doc)
    print(p.to_dict())



#Flatten the data so thweres not sublists in the attributes part

#Grabs all cities with state CA

#Create a reference to the cities collection
#cities_ref = db.collection("cities")

#Create a query against the collection
#query_ref = cities_ref.where(filter=FieldFilter("state", "==", "CA"))




