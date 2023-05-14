import argparse
import json
import xmlschema
import os.path

parser = argparse.ArgumentParser(
    prog="xml2json.py",
    description="convert XML files to JSON"
)

parser.add_argument("filename",
                    help="input XML file")
parser.add_argument("-s", "--schema", required=True,
                    help="XML Schema file (.xsd)")
parser.add_argument("-b", "--base", default="./",
                    help="XML Schema file base path (referenced XSD file will be searched here)")
parser.add_argument("-o", "--output", default="./",
                    help="output filename")

args = parser.parse_args()

assert os.path.exists(args.filename)
assert os.path.exists(os.path.join(args.base, args.schema))

xs = xmlschema.XMLSchema(args.schema, base_url=args.base)

with open(args.output, "w") as f:
    json.dump(xs.to_dict(args.filename, decimal_type=str), f)
