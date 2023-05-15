import pymongo
import json
import sys

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["ncbi"]
#mycol = mydb["biosample"]
mycol = mydb["bioproject"]

with open(sys.argv[1]) as f:
    dat = json.load(f)

#mycol.insert_many(dat["BioSample"])
for d in dat["Package"]:
    try:
        mycol.insert_one(d)
    except:
        print(d)
