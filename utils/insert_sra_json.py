import pymongo
import json
import sys
import re
import pathlib

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["ncbi"]

fname = pathlib.Path(sys.argv[1])
sra_accession, division = fname.stem.split(".")

mycol = mydb[f"sra_{division}"]

with open(sys.argv[1]) as f:
    dat = json.load(f)

dat.pop("@xmlns:xsi")
dat["SRA_ACCESSION"] = sra_accession

try:
    mycol.insert_one(dat)
except:
    print(fname)
