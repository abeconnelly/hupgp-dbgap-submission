#!/bin/bash

set -e
set -o pipefail

mkdir -p submission

echo "Downloading surveys from https://my.pgp-hms.org/google_surveys ..."
echo ""

# Grab survey data 
#
./src/grab_phenotype.sh

echo ""
echo "Surveys downloaded, generating submission files..."
echo ""

pushd src 2> /dev/null 1>&2
ln -f -s ../data .
ln -f -s ../submission .
ln -f -s ../config/Participant.list ./hu.list
ln -f -s ../config/hu_23andme.map
ln -f -s ../config/hu_cgi_sample.list
./generate_all.py
popd 2> /dev/null 1>&2


echo ""
echo "Submission files generated.  Check the 'submission' directory output"
echo ""
