from urllib.parse import quote_plus
from pymongo import MongoClient
import pprint
from bson.son import SON

# Programme principal
print("requete_db_api")

uri = "mongodb://%s:%s@%s" % ( quote_plus('root'), quote_plus('pwd_root'), 'mongo')
client = MongoClient(uri)
db = client.db_carburant
collection = db.pdv_api

lon = float(input("longitude: "))
lat = float(input("latitude: "))
dist = float(input("distance: "))
#lon = 4.406
#lat = 45.457
#dist = 10

query_dist = {"location": SON([("$near", [lon, lat]), ("$maxDistance", dist)])}
query_carburant = {'SP95_present': True}

query = { '$and': [ query_dist, query_carburant ] }

print("query: ",query)

for doc in collection.find(query).limit(5):
    pprint.pprint(doc)
