#!/usr/bin/python
#
# Create CSV file with all the (cleaned) pheontype
# data for participants in the 'hu.list' file.
#

import os
import re
import sys
import json
import subprocess as sp

def norm_ts(ts):
  m = re.match(r'^(\d+)\/(\d+)\/(\d+) (\d+):(\d+):(\d+)', ts)
  if not m:
    return ts
  ye = int(m.group(3))
  mo = int(m.group(1))
  da = int(m.group(2))
  HO = int(m.group(4))
  MI = int(m.group(5))
  SE = int(m.group(6))
  v = "{:0>4d}-{:0>2d}-{:0>2d} {:0>2d}:{:0>2d}:{:0>2d}".format(ye, mo, da, HO, MI, SE)
  return v


valid_huid = {}
phenotype = {}

# ...
#
fn_huid = "./hu.list"

with open(fn_huid) as fp:
  for line in fp:
    line = line.strip(' ')
    line = line.strip('\n')
    valid_huid[line]={"huID":line}



# The survey has a different format from the rest and will be treated
# specially.
#
fn_survey = "data/PGP_Participant_Survey.csv"
ofn_survey = "submission/2a_Participant_survey.txt"

# These files have similar formats so are processed at once.
#
fn_trait = [ "data/PGP_Trait_Disease_Survey_2012_Blood.csv",
"data/PGP_Trait_Disease_Survey_2012_Cancers.csv",
"data/PGP_Trait_Disease_Survey_2012_Circulatory_System.csv",
"data/PGP_Trait_Disease_Survey_2012_Congenital_Traits_and_Anomalies.csv",
"data/PGP_Trait_Disease_Survey_2012_Digestive_System.csv",
"data/PGP_Trait_Disease_Survey_2012_Endocrine_Metabolic_Nutritional_and_Immunity.csv",
"data/PGP_Trait_Disease_Survey_2012_Genitourinary_Systems.csv",
"data/PGP_Trait_Disease_Survey_2012_Musculoskeletal_System_and_Connective_Tissue.csv",
"data/PGP_Trait_Disease_Survey_2012_Nervous_System.csv",
"data/PGP_Trait_Disease_Survey_2012_Respiratory_System.csv",
"data/PGP_Trait_Disease_Survey_2012_Skin_and_Subcutaneous_Tissue.csv",
"data/PGP_Trait_Disease_Survey_2012_Vision_and_hearing.csv" ]

ofn_trait = [ "submission/2a_Blood.txt",
"submission/2a_Cancers.txt",
"submission/2a_Circulatory_System.txt",
"submission/2a_Congenital_Traits_and_Anomalies.txt",
"submission/2a_Digestive_System.txt",
"submission/2a_Endocrine_Metabolic_Nutritional_and_Immunity.txt",
"submission/2a_Genitourinary_Systems.txt",
"submission/2a_Musculoskeletal_System_and_Connective_Tissue.txt",
"submission/2a_Nervous_System.txt",
"submission/2a_Respiratory_System.txt",
"submission/2a_Skin_and_Subcutaneous_Tissue.txt",
"submission/2a_Vision_and_hearing.txt" ]

def get_dd_survey_header_line(dd):

  header_fields = [ "VARNAME", "VARDESC", "DOCFILE", "TYPE", "UNITS", "MIN", "MAX",
                    "RESOLUTION", "COMMENT1", "COMMENT2",
                    "VARIABLE_SOURCE", "SOURCE_VARIABLE_ID", "VARIABLE_MAPPING",
                    "UNIQUEKEY", "COLLINTERVAL", "ORDER", "VALUES" ]

  data_def = {
  "huID": { "VARNAME":"SUBJECT_ID", "VARDESC":"Subject ID",
    "TYPE":"string", "VARIABLE_SOURCE":"Harvard PGP",
    "SOURCE_VARIABLE_ID":"huID",
    "UNIQUEKEY":"X" },
  "timestamp": { "VARNAME":"TIMESTAMP", "VARDESC":"Time response was collected",
    "TYPE":"string", "VARIABLE_SOURCE":"Harvard PGP",
    "SOURCE_VARIABLE_ID":"timestamp", "UNIQUEKEY":"X" },
  "SUBJECT_ID": { "VARNAME":"SUBJECT_ID", "VARDESC":"Subject ID",
    "TYPE":"string", "VARIABLE_SOURCE":"Harvard PGP",
    "SOURCE_VARIABLE_ID":"huID",
    "UNIQUEKEY":"X" },
  "TIMESTAMP": { "VARNAME":"TIMESTAMP", "VARDESC":"Time response was collected",
    "TYPE":"string", "VARIABLE_SOURCE":"Harvard PGP",
    "SOURCE_VARIABLE_ID":"timestamp", "UNIQUEKEY":"X" },
  "Age": { "VARNAME":"Age", "VARDESC":"Reported age at time of survey",
    "TYPE":"string", "VARIABLE_SOURCE":"Harvard PGP",
    "SOURCE_VARIABLE_ID":"Age" },
  "Anatomical sex at birth": { "VARNAME":"Anatomical sex at birth", "VARDESC":"Reported anatomical sex at birth",
    "TYPE":"string", "VARIABLE_SOURCE":"Harvard PGP",
    "SOURCE_VARIABLE_ID":"Anatomical sex at birth" },
  "Month of birth": { "VARNAME":"Month of birth", "VARDESC":"Reported month of birth",
    "TYPE":"string", "VARIABLE_SOURCE":"Harvard PGP",
    "SOURCE_VARIABLE_ID":"Month of birth" },
  "Race/ethnicity": { "VARNAME":"Race/ethnicity", "VARDESC":"Reported race/ethnicity",
    "TYPE":"string", "VARIABLE_SOURCE":"Harvard PGP",
    "SOURCE_VARIABLE_ID":"Race/ethnicity" },
  "Sex/Gender": { "VARNAME":"Sex/Gender", "VARDESC":"Reported sex/gender",
    "TYPE":"string", "VARIABLE_SOURCE":"Harvard PGP",
    "SOURCE_VARIABLE_ID":"Sex/Gender" },
  "Year of birth": { "VARNAME":"Year of birth", "VARDESC":"Reported year of birth",
    "TYPE":"string", "VARIABLE_SOURCE":"Harvard PGP",
    "SOURCE_VARIABLE_ID":"Year of birth" },
  "DEFAULT": { "TYPE":"decimal, ecnoded value", "VARIABLE_SOURCE":"Harvard PGP",
    "ORDER":"List", "MIN":"0", "MAX":"1" }
  }

  emit_line = ""
  for i,h in enumerate(header_fields):
    if i>0: emit_line+="\t"
    if h in data_def[dd]:
      emit_line += data_def[dd][h]
  return emit_line



def get_dd_header_line(dd, descr=""):
  cols = ["VARNAME","VARDESC","DOCFILE","TYPE","UNITS","MIN","MAX","RESOLUTION","COMMENT1","COMMENT2","VARIABLE_SOURCE","SOURCE_VARIABLE_ID","VARIABLE_MAPPING","UNIQUEKEY","COLLINTERVAL","ORDER","VALUES"]

  default_val = { "TYPE" : "decimal, encoded value",
                  "MIN" : "0",
                  "MAX" : "1",
                  "VARIABLE_SOURCE" : "Harvard PGP",
                  "ORDER" : "List",
                  "VALUES" : "1=Reported 0=Not reported" }

  datatype = "decimal, encoded value"

  source_var_id = dd
  uniq = ""
  if len(descr)==0:
    descr = dd
  if dd == "SUBJECT_ID":
    descr = "Subject ID"
    datatype = "string"
    source_var_id = "huID"
    uniq="X"
  elif dd == "TIMESTAMP":
    descr = "Time response was collected"
    datatype = "string"
    source_var_id = "timestamp"
    uniq="X"

  emit_line = dd + "\t" + descr
  for h in cols[2:]:

    if h == "VARIABLE_SOURCE":
      emit_line += "\t" + default_val[h]
      continue
    if h == "SOURCE_VARIABLE_ID":
      emit_line += "\t" + source_var_id
      continue
    if h == "UNIQUEKEY":
      emit_line += "\t" + uniq
      continue
    if datatype=="string":
      emit_line += "\t"
      continue

    val = ""
    if h in default_val:
      val = default_val[h]
    emit_line += "\t" + val

  return emit_line




g_phenotype_class = {}


# Some fields span multiple lines, embedded in quotes.  fmt_lines.pl takes care of these
# fields, noticing when a line has a newline inside of a double quote.  It deletes
# the newline and puts the field element all on one line.
#
txt = sp.check_output( "./fmt_lines.pl " + fn_survey + " | csvtool col 1- -u TAB -", shell=True)
lines = txt.split("\n")
enum_phen = {}

phen_prefix = "Participant_Survey"

marked_survey_fields = { "Sex/Gender":1, "Race/ethnicity":1, "Month of birth":1, "Anatomical sex at birth":1, "Year of birth":1 }
header = ["SUBJECT_ID", "TIMESTAMP", "Sex/Gender", "Race/ethnicity", "Month of birth", "Anatomical sex at birth", "Year of birth" ]

ofp = open(ofn_survey, "w")

process_header = True
survey_header = []
for l in lines:
  field = l.split("\t")
  if len(field)==0 or len(field)==1:
    continue

  field_huid,raw_ts,uuid,survey = field[0], field[1], field[2], field[3:]
  ts = norm_ts(raw_ts)

  if process_header:
    emit_line = "SUBJECT_ID\tTIMESTAMP"
    for i in range(len(survey)):
      survey_header.append( survey[i] )

      if survey[i] in marked_survey_fields:
        emit_line += "\t" + survey[i]
    survey_header.append("none")
    process_header = False

    ofp.write(emit_line + "\n")

    continue


  #if field_huid not in huid[ts]:
  if field_huid not in valid_huid:
    continue


  if len(survey) > len(survey_header):
    print "ERROR: survey length > survey_header length:", field_huid, ts, uuid, len(survey), len(survey_header)
    print survey_header
    print survey
    sys.exit(0)

  # loop through survey columns
  #
  emit_line = field_huid + "\t" + ts
  for i in range(len(survey)):
    enum_column = phen_prefix + ":" + survey_header[i]

    s_field = survey[i].strip(' ')

    if len(s_field)==0:
      continue

    if survey_header[i] in marked_survey_fields:

      sh = survey_header[i]
      if re.search( r' [Yy]ears$', s_field ):
        sh = "Age"

      emit_line += "\t" + s_field


    enum_type = enum_column + ":" + s_field

    # replace commas with '%2C' (url-code for comma) when a comma appears
    # inside of a parenthsis string.
    #
    # For example:
    #
    #  Chronic tension headaches (15+ days per month, at least 6 months)
    #
    # will be replaced with:
    #
    #  Chronic tension headaches (15+ days per month%2C at least 6 months)
    #
    enum_type = re.sub( r'(\([^\)]*),([^\)]*\))', r'\1%2C\2', enum_type )

    # Diabetes mellitus has different types, indicated 'type [12]' (maybe more,
    # I've only observed 1 and 2) seperated by a comma.
    # For example "Daiabetes mellitus, type 1".
    #
    # Replace the prefix comma for 'type' with url encoded '%2C'.
    #
    enum_type = re.sub( r'Diabetes mellitus, type', r'Diabetes mellitus%2C type', enum_type)

    enum_type = enum_type.strip(' ')
    if len(enum_type) > 0:

      ## DEBUG
      g_phenotype_class[ phen_prefix + ":" + enum_type] = 1

      if enum_type in enum_phen:
        enum_phen[ enum_type ] += 1
      else:
        enum_phen[ enum_type ] = 1

  ofp.write(emit_line + "\n")

ofp = open(ofn_survey, "w")
ofn_dd = re.sub( r'2a_', r'2b_', ofn_survey)
ofp = open(ofn_dd, "w")
ofp.write("VARNAME\tVARDESC\tDOCFILE\tTYPE\tUNITS\tMIN\tMAX\tRESOLUTION\tCOMMENT1\tCOMMENT2\tVARIABLE_SOURCE\tSOURCE_VARIABLE_ID\tVARIABLE_MAPPING\tUNIQUEKEY\tCOLLINTERVAL\tORDER\tVALUES\n")
for h in header:
  l = get_dd_survey_header_line(h)
  ofp.write(l + "\n")
ofp.close()



# fn_trait file formats are of the form:
# HUID,Timestamp,UUID_CODE,EnumeratedType,FreeText
#  0      1          2          3           4
#
for pos,fn in enumerate(fn_trait):

  huid_ts_phen = {}

  # Some fields span multiple lines, embedded in quotes.  fmt_lines.pl takes care of these
  # fields, noticing when a line has a newline inside of a double quote.  It deletes
  # the newline and puts the field element all on one line.
  #
  txt = sp.check_output( "./fmt_lines.pl " + fn + " | csvtool col 1- -u TAB -", shell=True)
  lines = txt.split("\n")

  enum_phen = {}

  phen_prefix = re.sub( r'data/PGP_Trait_Disease_Survey_2012_(.*)\.csv', r'\1', fn )

  ofp = open(ofn_trait[pos], "w")

  header_map = {}
  process_header = True
  for l in lines:
    field = l.split("\t")
    if process_header:
      process_header = False
      continue

    if len(field)!=5:
      if len(field)>1:
        pass
      continue

    field_huid,raw_ts,uuid,enum_type,freetext = field

    ts = norm_ts(raw_ts)

    #if field_huid not in huid:
    if field_huid not in valid_huid:
      continue

    if field_huid not in huid_ts_phen:
      huid_ts_phen[field_huid] = {}
    if ts not in huid_ts_phen[field_huid]:
      huid_ts_phen[field_huid][ts] = { "huID": field_huid, "timestamp":ts }


    # Some fields have extra commas in them so we have to take special
    # consideration.
    #

    # replace commas with '%2C' (url-code for comma) when a comma appears
    # inside of a parenthsis string.
    #
    # For example:
    #
    #  Chronic tension headaches (15+ days per month, at least 6 months)
    #
    # will be replaced with:
    #
    #  Chronic tension headaches (15+ days per month%2C at least 6 months)
    #
    et_csv = re.sub( r'(\([^\)]*),([^\)]*\))', r'\1%2C\2', enum_type )

    # Diabetes mellitus has different types, indicated 'type [12]' (maybe more,
    # I've only observed 1 and 2) seperated by a comma.
    # For example "Daiabetes mellitus, type 1".
    #
    # Replace the prefix comma for 'type' with url encoded '%2C'.
    #
    et_csv = re.sub( r'Diabetes mellitus, type', r'Diabetes mellitus%2C type', et_csv)

    et_csv = re.sub( r'Infantile, juvenile, and presenile cataract', r'Infantile%2C juvenile%2C and presenile cataract', et_csv)

    for et in et_csv.split(","):
      et = et.strip(' ')

      if len(et) > 0:
        g_phenotype_class[ phen_prefix + ":" + et ] = 1
        huid_ts_phen[field_huid][ts][ phen_prefix + ":" + et ] = 1

      if et in enum_phen:
        enum_phen[et] += 1
      else:
        enum_phen[et] = 1

  header = [ "SUBJECT_ID", "TIMESTAMP" ]

  for phen_header in enum_phen:
    if len(phen_header) > 0:
      header.append(phen_header)

  ofp.write( "\t".join(header) + "\n" )

  for huid in huid_ts_phen:
    for ts in huid_ts_phen[huid]:
      emit_line = huid + "\t" + ts
      for h in header[2:]:

        val = "0"
        if (phen_prefix + ":" + h) in huid_ts_phen[huid][ts]: val = "1"
        emit_line += "\t" + val

      ofp.write( emit_line + "\n" )

  ofp.close()

  ofn_dd = re.sub( r'2a_', r'2b_', ofn_trait[pos])
  ofp = open(ofn_dd, "w")
  ofp.write("VARNAME\tVARDESC\tDOCFILE\tTYPE\tUNITS\tMIN\tMAX\tRESOLUTION\tCOMMENT1\tCOMMENT2\tVARIABLE_SOURCE\tSOURCE_VARIABLE_ID\tVARIABLE_MAPPING\tUNIQUEKEY\tCOLLINTERVAL\tORDER\tVALUES\n")
  for h in header:
    l = get_dd_header_line(h)
    ofp.write(l + "\n")
  ofp.close()
