# download BioSample XML from NCBI
ascp -l500m -T -k 1 -i /home1/panyuanfei/.conda/envs/yfpan/etc/asperaweb_id_dsa.openssh anonftp@ftp.ncbi.nlm.nih.gov:/biosample/biosample_set.xml.gz .

# alternative: using wget
# wget https://ftp.ncbi.nlm.nih.gov/biosample/biosample_set.xml.gz

gzip -d biosample_set.xml.gz

# parse XML schema from the BioSample XML file
java -jar trang.jar biosample_set.xml biosample.xsd

mkdir -p biosample_set
# split the BioSample XML file (it's too large to be processed at once)
python xml_split.py \
    -t BioSample \
    --template biosample_template.xml \
    -s 10000 \
    -o biosample_set \
    biosample_set.xml

# parse XML file to JSON
ls biosample_set \
    | grep "\.xml$" \
    | sed "s/.xml//g" \
    | parallel -j40 python xml2json.py -s biosample.xsd -o biosample_set_json/{}.json biosample_set/{}.xml

cd biosample_set_json
ls *.json | parallel 'sed "s/\"$\":/\"value\":/g" {} > {}.mod'
ls *.json | parallel 'rm {}'
ls *.json.mod | sed "s/.json.mod//g" | parallel mv {}.json.mod {}.json
cd ..

