#!/bin/bash

bdir="data"
for x in `ls $bdir`
do
  echo ""
  echo ">>>>>>>>>>>>> $bdir/$x"
  ./fmt_lines.pl $bdir/$x | head -n5 | csvtool col 1- -u TAB -
done

#./fmt_lines.pl data/PGP_Trait_Disease_Survey_2012_Cancers.csv  | pretform -d, 
