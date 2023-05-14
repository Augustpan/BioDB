import xml.etree.ElementTree as ET
import argparse
import os.path
from pathlib import Path

parser = argparse.ArgumentParser(
    prog="xml_split.py",
    description="split large XML file"
)

parser.add_argument("filename",
                    help="input XML file")
parser.add_argument("-t", "--tag", required=True,
                    help="split by <tag>")
parser.add_argument("-o", "--output", default="./",
                    help="output folder")
parser.add_argument("-s", "--size", default=1000, type=int,
                    help="batch size")
parser.add_argument("-p", "--prefix",
                    help="output file prefix")
parser.add_argument("--wrap-tail", nargs='*', help="XML header")
parser.add_argument("--wrap-head", nargs='*', help="XML footer")
parser.add_argument("--template", help="XML template file")
parser.add_argument("--placeholder", default="#PLACEHOLDER#")

args = parser.parse_args()

assert os.path.exists(args.filename)
assert os.path.exists(args.output)
if args.template:
    assert os.path.exists(args.template)
assert args.size > 0

if not args.prefix:
    args.prefix = Path(args.filename).stem + "_split_"

context = ET.iterparse(args.filename, events=('end', ))
index = 0
batch_size = args.size

elem_list = []
for event, elem in context:
    if elem.tag == args.tag:
        elem_list.append(ET.tostring(elem).decode())
        if len(elem_list) == batch_size:
            index += 1
            filename = os.path.join(args.output, f"{args.prefix}{index}.xml")
        
            # wrap xml file
            if args.template:
                with open(args.template) as f:
                    xml_template = f.read()
                xml_str = xml_template.replace(args.placeholder, "".join(elem_list))
            else:
                xml_str = ""
                if args.wrap_head:
                    for line in args.wrap_head:
                        xml_str += f"{line.strip()}\n"
                xml_str += "".join(elem_list)
                if args.wrap_tail:
                    for line in args.wrap_tail:
                        xml_str += f"{line.strip()}\n".encode()
            
            # output
            with open(filename, 'wb') as f:
                f.write(xml_str.encode())

            elem_list = []
