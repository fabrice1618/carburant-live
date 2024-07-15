import time
import util
import get_xml

def test_job():
    util.log('test', "test_job" )

# Configuration backend
#PERIODE = 10 * 60       # soit 10 minutes
PERIODE = 60 * 60       # test 1 heure
FICHIER_XML = "/data/PrixCarburants_instantane.xml"
TIME_INIT = ( 2022, 1, 1, 23, 58, 0, 0, 0, 0 )

util.log('Starting backend', 'backend')

uri = "mongodb://%s:%s@%s" % ( quote_plus('root'), quote_plus('pwd_root'), 'mongo')
client = MongoClient(uri)
db = client.db_carburant
collection = db.pdv_opendata

debut = time.mktime(TIME_INIT)

while True:
    if time.time() - debut > PERIODE:
        test_job()
        get_xml.download(FICHIER_XML)
        read_xml.xml_parse(FICHIER_XML)
        debut = time.time()

    time.sleep(1)
