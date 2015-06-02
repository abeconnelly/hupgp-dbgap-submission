#!/usr/bin/python
#
# Regenerate all the relevant files for the dbGaP submission/
#
# Output is in the 'submission' sub-directory.
#

import subprocess as sp
import re

def write_to_file(fn, s):
  fp = open(fn, "w")
  fp.write(s)
  fp.close()


s = sp.check_output( ["./create_phenotype.py"] )

s = sp.check_output( ["./3ab_generate.py"] )
xy = re.split( '^====*\n', s, flags=re.M )
write_to_file("submission/3a_dbGaP_SampleAttributes.txt", xy[0])
write_to_file("submission/3b_dbGaP_SampleAttributes.txt", xy[1])

s = sp.check_output( ["./4ab_generate.py"] )
xy = re.split( '^====*\n', s, flags=re.M )
write_to_file("submission/4a_dbGaP_Subject.txt", xy[0])
write_to_file("submission/4b_dbGaP_Subject.txt", xy[1])

s = sp.check_output( ["./5ab_generate.py"] )
xy = re.split( '^====*\n', s, flags=re.M )
write_to_file("submission/5a_dbGaP_SubjectSampleMappings.txt", xy[0])
write_to_file("submission/5b_dbGaP_SubjectSampleMappings.txt", xy[1])
