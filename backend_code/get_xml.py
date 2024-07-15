import requests, zipfile, io
import os
import util

def download(fichier_xml):
    url = "https://donnees.roulez-eco.fr/opendata/instantane"

    util.log('starting', 'get_xml')

    if os.path.exists(fichier_xml):
        os.unlink(fichier_xml)

    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall("/data")

    statinfo = os.stat(fichier_xml)
    util.log(f"filename : {fichier_xml} filesize : {statinfo.st_size}", 'get_xml')

if __name__ == '__main__':
    FICHIER_XML = "/data/PrixCarburants_instantane.xml"
    download(FICHIER_XML)

