import xml.sax
import os
from urllib.parse import quote_plus
from pymongo import MongoClient
import pprint
import datetime

class LecteurSax(xml.sax.ContentHandler):
    def resetPdv(self):
        self.pdv = dict()
        self.cur_element = ""
        self.liste_services = []
        self.liste_prix = []
        self.liste_jours = []
        self.liste_horaires = []
        self.jour_id = 0

    def findDiff(self, db_pdv):
        exclude_fields = ["_id","id","liste_horaires","liste_jours","liste_services","date_created", "date_update"]
        nb_supp = 0
        nb_add = 0
        nb_diff = 0

#        print("********* findDiff")
#        pprint.pprint(db_pdv)
        
        for cle, valeur in db_pdv.items():
            if not cle in exclude_fields \
                and not cle in self.pdv.keys():

                print("********* findDiff delete", cle, "=", valeur)
                nb_supp += 1

        for cle, valeur in self.pdv.items():
            if  not cle in exclude_fields \
                and not cle in db_pdv:

                print("********* findDiff new:", cle, valeur)
                nb_add += 1

        for cle, valeur in self.pdv.items():

            if  not cle in exclude_fields and cle in db_pdv:
                if valeur != db_pdv[cle]:
                    print("********* findDiff update:", cle)
                    pprint.pprint(valeur)
                    print("->")
                    pprint.pprint(db_pdv[cle])

                    nb_diff += 1

#        if nb_diff + nb_add + nb_supp == 0:
#            print("********* Point de vente identique", self.pdv['id'])
            #pprint.pprint(db_pdv)

        return(nb_diff + nb_add + nb_supp)

    def date_update(self):
#        print("--- date_update")
#        pprint.pprint(self.pdv)
        
        date_update = None
    
        for cle, valeur in enumerate(self.pdv['liste_prix']):
            if date_update is None or date_update < valeur['maj']:
                date_update = valeur['maj']
            
        return(date_update)

    def persist(self):
        global collection

#        print("== self Point de vente ==")
#        pprint.pprint(self.pdv)
        self.pdv['date_update'] = self.date_update()

        db_pdv = collection.find_one({"id": self.pdv['id']})
        if not db_pdv is None:
            if self.findDiff(db_pdv) > 0:
                # MAJ si difference detectee
                if 'date_created' in db_pdv:
                    self.pdv['date_created'] = db_pdv['date_created']
                else:
                    self.pdv['date_created'] = datetime.datetime.now()

                result = collection.delete_one({"id": self.pdv['id']})
                pdv_id = collection.insert_one(self.pdv).inserted_id

        else:
            print("********* Nouveau point de vente", self.pdv['id'])
            self.pdv['date_created'] = datetime.datetime.now()
            pdv_id = collection.insert_one(self.pdv).inserted_id
            #print("insert pdv_id:", pdv_id)


    def __init__(self):
        self.pdv_count = 0
        self.resetPdv()

    def startDocument(self):
        print( "Start document parsing" )

    def startElement(self, name, attrs):
        self.cur_element = name

        if name == "pdv":
            self.resetPdv()
            self.pdv = dict(attrs)

        elif name == "prix":
            self.liste_prix.append( dict(attrs) )

        elif name == "horaires":
            attributs = dict(attrs)
            self.pdv['automate_24_24'] = attributs['automate-24-24']

        elif name == "jour":
            attributs = dict(attrs)
            self.liste_jours.append(attributs)
            self.jour_id = attributs['id']

        elif name == "horaire":
            attributs = dict(attrs)
            attributs['id'] = self.jour_id
            self.liste_horaires.append(attributs)


    def endElement(self, name):
        self.cur_element = ""

        if name == "pdv":
            self.pdv['liste_services'] = self.liste_services
            self.pdv['liste_prix'] = self.liste_prix
            self.pdv['liste_jours'] = self.liste_jours
            self.pdv['liste_horaires'] = self.liste_horaires

            self.persist()

            self.pdv_count += 1
            self.resetPdv()

    def characters(self, content):
        if self.cur_element == "adresse":
            self.pdv['adresse'] = content
        elif self.cur_element == "ville":
            self.pdv['ville'] = content
        elif self.cur_element == "service":
            self.liste_services.append(content)

    def endDocument(self):
        print("Nombre de PDV : {}".format(self.pdv_count))
        print( "End document parsing" )


# Programme principal

print("Hello SAX")
fichier_xml = "files/PrixCarburants_instantane.xml"

statinfo = os.stat(fichier_xml)
print("filesize : {}".format(statinfo.st_size))

uri = "mongodb://%s:%s@%s" % ( quote_plus('root'), quote_plus('pwd_root'), 'mongo')
client = MongoClient(uri)
db = client.db_carburant
collection = db.pdv_opendata

parser = xml.sax.make_parser()
lecteurSax = LecteurSax()
parser.setContentHandler(lecteurSax)
parser.parse(fichier_xml)

exit()
