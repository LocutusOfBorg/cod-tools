#!/bin/sh

scripts/cif_molecule \
    -i \
    --max-polymer-atoms=200 \
    --max-polymer-span=2 \
    --one-datablock-output \
    tests/inputs/polymers/7051216.cif