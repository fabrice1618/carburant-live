import time
import requests, zipfile, io
import os

periode = 10 * 60       # soit 10 minutes

def get_xml():
    global fichier_xml;

    print( "get_xml(): ", time.strftime("%H:%M:%S") )
    os.unlink(fichier_xml)

    url = "https://donnees.roulez-eco.fr/opendata/instantane"
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall("files")

    print( os.listdir("files") )

    statinfo = os.stat(fichier_xml)
    print("filesize : {}".format(statinfo.st_size))
    

# Programme principal
fichier_xml="files/PrixCarburants_instantane.xml"

get_xml()
debut = time.time()

while True:

    if time.time() - debut > periode:
        # Appel toutes les 10 minutes
        get_xml()
        debut = time.time()

    time.sleep(42)
