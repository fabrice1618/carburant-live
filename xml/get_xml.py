import time
import requests, zipfile, io
import os

periode = 10 * 60 # 10 minutes

def get_xml():
    print( "get_xml(): ", time.strftime("%H:%M:%S") )
    fichier="PrixCarburants_instantane.xml"
    os.unlink("files/"+fichier)

    url = "https://donnees.roulez-eco.fr/opendata/instantane"
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall("files")

    print( os.listdir("files") )
    


# Programme principal
get_xml()
debut = time.time()

while True:

    if time.time() - debut > periode:
        # Appel toutes les 10 minutes
        get_xml()
        debut = time.time()

    time.sleep(42)
