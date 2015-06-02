#!/usr/bin/python

import sys

header = ["SUBJECT_ID", "SAMPLE_ID", "SAMPLE_SOURCE", "SOURCE_SAMPLE_ID", "SAMPLE_USE" ]
#header = ["SUBJECT_ID", "SAMPLE_ID", "SAMPLE_SOURCE", "SAMPLE_USE" ]

huid = []

fp = open("hu.list")
for l in fp:
  huid.append( l.strip(' ').strip('\n') )
fp.close()

tam_map = {}
fp = open("hu_23andme.map")
for l in fp:
  f = l.strip(' ').strip('\n').split(' ')
  tam_map[f[0]] = f[1]
fp.close

cgi_map = { "hu0E7AAF" : "GS03023-DNA_A01",
    "hu83BC6A" : "GS03023-DNA_C01",
    "hu9E6329" : "GS03052-DNA_A01",
    "hu826751" : "GS03052-DNA_B01",
    "hu7379BC" : "GS03052-DNA_E01",
    "hu7C3A81" : "GS03052-DNA_F01",
    "huB1488D" : "GS03052-DNA_H01",
    "hu8A5FBF" : "GS03184-DNA_A02",
    "hu3DC5EA" : "GS03184-DNA_F01",
    "hu925B56" : "GS03274-DNA_B01",
    "hu566AA7" : "GS03274-DNA_H01" }

header_str = ""
for i,h in enumerate(header):
  if i>0: header_str += "\t"
  header_str += h
print header_str


for hu in huid:
  print hu + "\t" + tam_map[hu] + "\t" + "Harvard Personal Genome Project" + "\t" + tam_map[hu] + "\t" + "SNP"

for hu in huid:
  print hu + "\t" + cgi_map[hu] + "\t" + "Harvard Personal Genome Project" + "\t" + cgi_map[hu] + "\t" + "WholeGenome"




#print "\n\n==============================================\n\n"
print "=============================================="


print "VARNAME\tVARDESC\tTYPE\tVALUES"
print "SUBJECT_ID\tSubject ID\tstring\t"
print "SAMPLE_ID\tSample ID\tstring\t"
print "SAMPLE_SOURCE\tSource of sample\tstring\t"
print "SOURCE_SAMPLE_ID\tSample ID used in the Source Repository\tstring\t"
print "SAMPLE_USE\tSample use\tencoded values\t"

#print "\n\n"


