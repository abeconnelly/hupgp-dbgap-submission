#!/usr/bin/python

import re
import sys

data_field = ["SAMPLE_ID", "ANALYTE_TYPE", "COMPANY_DATA_SOURCE", "IS_TUMOR" ]

sample_id = []

hu23am_fp = open("hu_23andme.map")
for l in hu23am_fp:
  l = l.strip()
  f = l.split(' ')
  #print l, f[0], f[1]
  sample_id.append(f[1])
hu23am_fp.close()

#sample_id = [ "hu0E7AAF.23andme",
#    "hu3DC5EA.23andme",
#    "hu566AA7.23andme",
#    "hu7379BC.23andme",
#    "hu7C3A81.23andme",
#    "hu826751.23andme",
#    "hu83BC6A.23andme",
#    "hu8A5FBF.23andme",
#    "hu925B56.23andme",
#    "hu9E6329.23andme",
#    "huB1488D.23andme",
#    "GS03023-DNA_A01",
#    "GS03023-DNA_C01",
#    "GS03052-DNA_A01",
#    "GS03052-DNA_B01",
#    "GS03052-DNA_E01",
#    "GS03052-DNA_F01",
#    "GS03052-DNA_H01",
#    "GS03184-DNA_A02",
#    "GS03184-DNA_F01",
#    "GS03274-DNA_B01",
#    "GS03274-DNA_H01" ]

cgi_sample_id = [ "GS03023-DNA_A01",
    "GS03023-DNA_C01",
    "GS03052-DNA_A01",
    "GS03052-DNA_B01",
    "GS03052-DNA_E01",
    "GS03052-DNA_F01",
    "GS03052-DNA_H01",
    "GS03184-DNA_A02",
    "GS03184-DNA_F01",
    "GS03274-DNA_B01",
    "GS03274-DNA_H01" ]

for z in cgi_sample_id:
  sample_id.append(z)

header_s = ""
for i,df in enumerate(data_field):
  if i>0: header_s += "\t"
  header_s += df
print header_s


for s in sample_id:
  col_s = ""
  for i,df in enumerate(data_field):
    if i>0: col_s += "\t"

    if df == "SAMPLE_ID":
      col_s += s
      continue

    if df == "ANALYTE_TYPE":
      col_s += "DNA"
      continue

    if df == "COMPANY_DATA_SOURCE":
      if re.search( r'\.23andme', s):
        col_s += "23andMe"
      else:
        col_s += "CGI"
      continue

    # "Y" for tumor
    # "N" for normal tissue
    #
    # All samples are normal tissue
    #
    if df == "IS_TUMOR":
      col_s += "N"


  print col_s

#print "\n\n==================================================\n\n"
print "=================================================="

## B PORTION
## Data defintion file
##

data_field = ["SAMPLE_ID", "ANALYTE_TYPE", "COMPANY_DATA_SOURCE", "IS_TUMOR" ]

header = [
  "VARNAME", "VARDESC", "DOCFILE", "TYPE", "UNITS", "MIN", "MAX", "RESOLUTION",
  "COMMENT1", "COMMENT1", "VARIABLE_SOURCE", "VARIABLE_TERM",
  "UNIQUEKEY", "COLLINTERVAL", "ORDER", "VALUES" ]

data_def = {
    "SAMPLE_ID" : { "VARNAME" : "SAMPLE_ID", "VARDESC" : "Sample ID", "TYPE": "string" },
    "ANALYTE_TYPE" : { "VARNAME" : "ANALYTE_TYPE", "VARDESC" : "Analyte Type", "TYPE": "string" },
    "COMPANY_DATA_SOURCE" : { "VARNAME" : "COMPANY_DATA_SOURCE", "VARDESC" : "Company responsible for generating the data", "TYPE": "string" },
    "IS_TUMOR" : { "VARNAME" : "IS_TUMOR", "VARDESC":"Tumor status", "TYPE" : "encoded values", "VALUES": "N=Is not a tumor,Y=Is Tumor" },
    "DEFAULT" : { "TYPE": "string" } }

header_s = ""
for i,h in enumerate(header):
  if i>0: header_s += "\t"
  header_s += h

print header_s

for df in data_field:
  col_s = ""

  if df in data_def:
    for i,h in enumerate(header):
      if i>0: col_s += "\t"
      if h in data_def[df]:
        col_s += data_def[df][h]
      else:
        col_s += ""
  else:
    pass

  print col_s
