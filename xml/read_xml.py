import xml.sax
import os
from urllib.parse import quote_plus
from pymongo import MongoClient

class LecteurSax(xml.sax.ContentHandler):
    def resetPdv(self):
        self.pdv = dict()
        self.cur_element = ""
        self.liste_services = []
        self.liste_prix = []
        self.liste_jours = []
        self.liste_horaires = []
        self.jour_id = 0

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
        global collection

        self.cur_element = ""

        if name == "pdv":
            self.pdv['liste_services'] = self.liste_services
            self.pdv['liste_prix'] = self.liste_prix
            self.pdv['liste_jours'] = self.liste_jours
            self.pdv['liste_horaires'] = self.liste_horaires

#            print("== Point de vente ==")
#            print(self.pdv)
            pdv_id = collection.insert_one(self.pdv).inserted_id
            print("insert pdv_id:", pdv_id)

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
collection = db.pdvs

parser = xml.sax.make_parser()
lecteurSax = LecteurSax()
parser.setContentHandler(lecteurSax)
parser.parse(fichier_xml)

exit()
