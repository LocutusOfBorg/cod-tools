#!/bin/sh

sudo apt-get install -y \
    curl \
    gawk \
    libcarp-assert-perl \
    libclone-perl \
    libdata-compare-perl \
    libdate-calc-perl \
    libdatetime-format-rfc3339-perl \
    libdbd-mysql-perl \
    libdbd-sqlite3-perl \
    libdbi-perl \
    libdigest-sha-perl \
    libhtml-parser-perl \
    libjson-perl \
    liblist-moreutils-perl \
    libmath-bigint-gmp-perl \
    libparse-yapp-perl \
    libtext-unidecode-perl \
    libwww-curl-perl \
    libxml-simple-perl \
    openbabel \
    perl \
    python-argparse \
    libmath-bigint-gmp-perl \
;

# The 'libmath-bigint-gmp-perl' package is not explicitly required,
# but it greatly improves the speed of BigRat arithmetics
