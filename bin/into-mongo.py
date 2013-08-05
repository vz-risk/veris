import pymongo
import json
import os

SERVER = 'localhost'
DATABASE = 'kevin'
COLLECTION = 'vcdb'

server = pymongo.Connection(SERVER)
db = server[DATABASE]
col = db[COLLECTION]


for (path, dirs, files) in os.walk('../vcdb'):
    for file in files:
        print('loading: '+os.path.join('../vcdb',file))
        infile = open(os.path.join('../vcdb',file), 'rb')
        incident = json.loads(infile.read())
        col.insert(incident)
