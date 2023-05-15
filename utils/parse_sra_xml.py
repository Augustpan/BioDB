import xmlschema
from pathlib import Path
import pickle
import os
import re
import json
import sys

if os.path.exists("SRA15_XSD/schema_dict.pkl"):
    with open("SRA15_XSD/schema_dict.pkl", "rb") as f:
        schema_dict = pickle.load(f)
else:
    schema_dict = {}
    for xsd_file in Path("SRA15_XSD").glob("SRA.*.xsd"):
        schema_name = xsd_file.stem.replace("SRA.", "")
        schema_dict[schema_name] = xmlschema.XMLSchema(xsd_file.stem+xsd_file.suffix, base_url="SRA15_XSD")
    with open("SRA15_XSD/schema_dict.pkl", "wb") as f:
        pickle.dump(schema_dict, f)
        
regex = re.compile(r"^([A-Z0-9]+)\.([a-z]+)$")

def parse_one(fname):
    fpath = Path(fname)
    match = regex.match(fpath.stem)
    if match:
        accession = match.group(1)
        schema_type = match.group(2)
        try:
            data_dct = schema_dict[schema_type].to_dict(fpath)
        except:
            print(f"parse_error: {fname}")
    else:
        print(f"file_error: {fname}")
    
    if data_dct:
        return accession, schema_type, json.dumps(data_dct)

fname = sys.argv[1]
ret = parse_one(fname)
if ret:
    accession, schema_type, json_str = ret
    with open(f"{sys.argv[2]}/{accession}.{schema_type}.json", "w") as f:
        f.write(json_str)
