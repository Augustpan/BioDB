# download BioProject XML and Schemas from NCBI
ascp -l500m -T -k 1 -i /home1/panyuanfei/.conda/envs/yfpan/etc/asperaweb_id_dsa.openssh anonftp@ftp.ncbi.nlm.nih.gov:/bioproject/OLD_XML .

# alternative: using wget
# wget https://ftp.ncbi.nlm.nih.gov/bioproject/OLD_XML/core_bioproject.xml

cat OLD_XML/core_bioproject.xml \
    | sed -zE "s#<Project>\n\s*<Project>#<Project>#g" \
    | sed -zE "s#</Project>\n\s*</Project>#</Project>#g" \
    > OLD_XML/core_bioproject_simplified.xml

java -jar trang.jar OLD_XML/core_bioproject_simplified.xml OLD_XML/core_bioproject_simplified.xsd

mkdir -p core_bioproject_simplified
# split the BioProject XML file (it's too large to be processed at once)
python xml_split.py \
    -t Package \
    --template bioproject_old_template.xml \
    -s 10000 \
    -o core_bioproject_simplified \
    OLD_XML/core_bioproject_simplified.xml

mkdir -p core_bioproject_json
# parse XML file to JSON
ls core_bioproject_simplified \
    | grep "\.xml$" \
    | sed "s/.xml//g" \
    | parallel -j 40 python xml2json.py -s core_bioproject_simplified.xsd -b OLD_XML -o core_bioproject_json/{}.json core_bioproject_simplified/{}.xml

cd core_bioproject_json
ls *.json | parallel 'sed "s/\"$\":/\"value\":/g" {} > {}.mod'
ls *.json | parallel 'rm {}'
ls *.json.mod | sed "s/.json.mod//g" | parallel mv {}.json.mod {}.json
cd ..
