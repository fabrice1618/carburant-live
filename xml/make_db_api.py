from urllib.parse import quote_plus
from pymongo import MongoClient
import pprint
import string

# Programme principal
print("make_db_api")

uri = "mongodb://%s:%s@%s" % ( quote_plus('root'), quote_plus('pwd_root'), 'mongo')
client = MongoClient(uri)
db = client.db_carburant
source = db.pdv_opendata
dest = db.pdv_api

# Vidage de la collection pdv_api
dest.delete_many({})

for spdv in source.find():
    #pprint.pprint(spdv)
    dpdv = {}
    dpdv['id'] = spdv['id']
    dpdv['adresse'] = spdv['adresse']
    dpdv['cp'] = spdv['cp']
    dpdv['date_update'] = spdv['date_update']
    dpdv['ville'] = spdv['ville']
    if spdv['pop'] == 'A':
        dpdv['autoroute'] = True
    else:
        dpdv['autoroute'] = False

    dpdv['location'] = [
        float(spdv['longitude']) / 100000,
        float(spdv['latitude']) / 100000 ]

    liste_carburants = {
        'GAZOLE': {'present': False, 'prix': 0},
        'E85': {'present': False, 'prix': 0},
        'E10': {'present': False, 'prix': 0},
        'SP98': {'present': False, 'prix': 0},
        'GPLC': {'present': False, 'prix': 0},
        'SP95': {'present': False, 'prix': 0}
    }

    for cle, carburant in enumerate( spdv['liste_prix'] ):
        carb_name = carburant['nom'].upper()
        liste_carburants[carb_name]['present'] = True
        liste_carburants[carb_name]['prix'] = float(carburant['valeur'])

    for cle, carburant in liste_carburants.items():
        dpdv[cle + '_present'] = carburant['present']
        dpdv[cle + '_prix'] = carburant['prix']

    pdv_id = dest.insert_one(dpdv).inserted_id

exit()
