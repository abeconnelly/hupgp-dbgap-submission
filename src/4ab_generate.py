#!/usr/bin/python

header = [ "SUBJECT_ID", "CONSENT" ]

print header[0] + "\t" + header[1]
fp = open( "hu.list" )
for l in fp:
  huid = l.strip(' ').strip('\n')
  print huid + "\t" + "999"
fp.close()

#print "\n\n==================================\n\n"
print "=================================="


print "VARNAME\tVARDESC\tTYPE\tVALUES"
print "SUBJECT_ID\tSubject ID\tstring\t"
print "CONSENT\tConset group as determined by DAC\tencoded value\t999=Fully Public Release"
#print "\n\n"
