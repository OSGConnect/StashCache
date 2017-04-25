# order of things to be sent:
# filename
# filesize [bytes]
# time it took to copy [seconds] (float)
# computing site
# stashCache address used
#

fname='asdf/asdf/asdf/asdf/asdf/'
fsize=123123123
tcopy=123.1234
cs=MWT2
sc="stashCache1.org"

hn=$(hostname)
timestamp=$(date +%s)
header="[{ \"headers\" : {\"timestamp\" : \"${timestamp}\", \"host\" : \"${hn}\" },"
body="\"body\" : \"${timestamp},${fname},${fsize},${tcopy},${cs},${sc}\" }]"
body="\"body\" : { \"timestamp\" : \"${timestamp}\", \"filename\" : \"${fname}\", \"filesize\" : \"${fsize}\", \"copytime\" : \"${tcopy}\", \"cs\" : \"${cs}\", \"sc\" :\"${sc}\" } }]"

echo $header$body > data.json

curl -X POST -H 'Content-Type: application/json; charset=UTF-8' http://hadoop-dev.mwt2.org:80/ -d @data.json
rm data.json
