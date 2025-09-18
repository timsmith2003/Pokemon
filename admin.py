from google.cloud.firestore_v1.base_query import FieldFilter
import json
import authentication

db = authentication.db.collection("pokemon")

with open('pokedex.json') as data_file:    
    data = json.load(data_file)
    for v in data:
        doc_ref = db.document(str(v["name"]))
        doc_ref.set(v)

# This code brings data back in
docs = (
    db.where(filter=FieldFilter("name", "==", "Venusaur")).stream()
)

for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")

large_us_cities_query = db.where(
    filter=FieldFilter("state", "==", "CA")
).where(filter=FieldFilter("population", ">", 1000000))

#Flatten the data so thweres not sublists in the attributes part

#Grabs all cities with state CA

#Create a reference to the cities collection
#cities_ref = db.collection("cities")

#Create a query against the collection
#query_ref = cities_ref.where(filter=FieldFilter("state", "==", "CA"))




