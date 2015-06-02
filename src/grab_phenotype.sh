#!/bin/bash
#
# It's easier to convert to the HTML/XML to JSON then parse
# it that way.
#
# Download the survey page, parse out name and download
# links.  Delete weird characters in name and replace
# spaces with underscores.  Download CSV and name
# it the apprpriate csv file.
#

set -e
set -o pipefail

mkdir -p data

url="https://my.pgp-hms.org"

while read line
do
  nam=`echo "$line" | jq -r .name`
  link=`echo "$line" | jq -r .dl`

  clean_name=`echo "$nam" | tr -d '&:' | sed 's/  */_/g' `

  echo "$clean_name $link"

  wget -q "$url/$link" -O data/$clean_name.csv

done < <( wget -q "$url/google_surveys" -O - | xml2json | jq -c '.html.body.div[0].div[2].table.tbody.tr[] | { "name" : .td[0].a["#text"], "dl" : .td[5].a["@href"] }' )

