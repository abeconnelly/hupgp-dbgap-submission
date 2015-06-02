#!/usr/bin/python

import os
import sys
import re

url_cgi = {}
url_23andme = {}

phen_23andme_map = {}
phen_cgi_map = {}

fp = open("data/data_locations.csv")
for line in fp:
  line = line.strip()

  a = line.split(",")
  if a[1] == "cgi":
    url_cgi[a[0]] = a[2]
  elif a[1] == "23andme":
    url_23andme[a[0]] = a[2]
fp.close()

first=True
fp = open("dbgap_file_submission_txt/5a_dbGaP_SubjectSampleMappings.txt")
for line in fp:
  line = line.strip()
  a = line.split("\t")
  if first:
    first = False
    continue
  if re.search( r'23andme', a[1]):
    phen_23andme_map[a[0]] = a[1]
  else:
    phen_cgi_map[a[0]] = a[1]
fp.close()


print "SUBJECT_ID\tSAMPLE_ID\tURL"

for x in url_cgi:
  print x + "\t" + phen_cgi_map[x] + "\t" + url_cgi[x]

for x in url_23andme:
  print x + "\t" + phen_23andme_map[x] + "\t" + url_23andme[x]
