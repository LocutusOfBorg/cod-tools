#!/bin/sh
#------------------------------------------------------------------------------
#$Author$
#$Date$ 
#$Revision$
#$URL$
#------------------------------------------------------------------------------
#*
#* Test the way the 'cif_find_duplicates' handles entries that have been
#* explicitly marked as enantiomers by the COD maintainers both in the
#* checked entries and in the reference entries.
#**

#BEGIN DEPEND------------------------------------------------------------------
INPUT_SCRIPT=scripts/cif_find_duplicates
INPUT_NEW_CIF_DIR=tests/inputs/cif_find_duplicates/enantiomers/marked
INPUT_REF_CIF_DIR=tests/inputs/cif_find_duplicates/enantiomers/marked
#END DEPEND--------------------------------------------------------------------

set -ue

unset LANG
unset LC_CTYPE

${INPUT_SCRIPT} \
    ${INPUT_NEW_CIF_DIR} \
    ${INPUT_REF_CIF_DIR} \
| sort
