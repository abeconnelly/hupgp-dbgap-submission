Harvard Personal Genome Project (PGP Harvard) database of Genotypes and Phenotypes (dbGaP) Release v1
===

The Harvard Personal Genome Project is working with NCBI to make available data through the NCBI's dbGaP archive.

The purpose of the scripts in this repository is to collect the publicly available phenotype information for
submission to dbGaP.

All relevant files submitted to dbGaP should be available in the `submission` directory.  The scripts
to generate these files in the `submission` directory are included.

The dbGaP accession assigned to this study is [phs000905.v1.p1](http://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs000905.v1.p1).


Quickstart
---

The files are already generated and available in the `submission` directory but can be regenerated
if need be.

To download the phenotype information from the Harvard PGP site and create the appropriate files for
the dbGaP submission, run:

```bash
$ git clone https://github.com/abeconnelly/hupgp-dbgap-submission
$ cd hupgp-dbgap-submission
$ ./HUPGP-dbGaP-Download-and-Collect.sh
```

This will download the publicly available surveys available at the [Participant surveys page from the Harvard Personal Genome Project](https://my.pgp-hms.org/google_surveys)
and collect them in the `data` directory.  This should roughly be ~3Mb.

Once the survey information is collected, the survey information specific to the 11 participants, as listed in the `Participant.list` file, will be collected and
deposited in the `submission` directory.

Here is a sample run:

```bash
~/hupgp-dbgap-submission$ ./HUPGP-dbGaP-Download-and-Collect.sh
Downloading surveys from https://my.pgp-hms.org/google_surveys ...

PGP_Participant_Survey /google_surveys/1/download
PGP_Trait_Disease_Survey_2012_Cancers /google_surveys/6/download
PGP_Trait_Disease_Survey_2012_Endocrine,_Metabolic,_Nutritional,_and_Immunity /google_surveys/7/download
PGP_Trait_Disease_Survey_2012_Blood /google_surveys/8/download
PGP_Trait_Disease_Survey_2012_Nervous_System /google_surveys/9/download
PGP_Trait_Disease_Survey_2012_Vision_and_hearing /google_surveys/10/download
PGP_Trait_Disease_Survey_2012_Circulatory_System /google_surveys/11/download
PGP_Trait_Disease_Survey_2012_Respiratory_System /google_surveys/12/download
PGP_Trait_Disease_Survey_2012_Digestive_System /google_surveys/13/download
PGP_Trait_Disease_Survey_2012_Genitourinary_Systems /google_surveys/14/download
PGP_Trait_Disease_Survey_2012_Skin_and_Subcutaneous_Tissue /google_surveys/15/download
PGP_Trait_Disease_Survey_2012_Musculoskeletal_System_and_Connective_Tissue /google_surveys/16/download
PGP_Trait_Disease_Survey_2012_Congenital_Traits_and_Anomalies /google_surveys/17/download

Surveys downloaded, generating submission files...


Submission files generated.  Check the 'submission' directory output


```

Overview
---

dbGaP has submission guidelines and examples which can be found in the `documentation` directory.

Relevant to this submission, there are 5 'classes' of file type:

  - The study config document (the files with a '1' prefix)
  - The phenotype data and document data type files (the files with '2a' and '2b' prefixes)
  - The sample attributes data and document data type files (the files with '3a' and '3b' prefixes)
  - The subject data and document data type files (the files with '4a' and '4b' prefixes)
  - The subject sample mapping files (the files with a '5a' and '5b' prefixes)

The surveys download from the Harvard Personal Genome Project site are used in creating the phenotype files.
There is one phenotype data and document data type file per survey.

The sample attributes gives information about the sample types.  For this submission we included
the 23andMe and whole genomes received from CGI.

The subject files are used to indicate the consent of the participant.  In this case, '999' is the
code for 'Fully Public Release' also described in the document data type file, `4b_dbGaP_Subject.txt`.

the subject sample mapping file maps the participants ID to the corresponding sample files.


Non-Standard Dependencies
---

  - csvtool
  - [jq](http://stedolan.github.io/jq/) http://stedolan.github.io/jq/
  - [xml2json](https://github.com/Cheedoong/xml2json) https://github.com/Cheedoong/xml2json

Licence
---

All code is under an AGPLv3.0 license.  See the `LICENSE.txt` for details.

All data is released under a CC0 license.
