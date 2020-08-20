#!/bin/bash

#BEGIN DEPEND------------------------------------------------------------------

INPUT_PRECISION=src/lib/perl5/COD/Precision.pm
INPUT_PRINT=src/lib/perl5/COD/CIF/Tags/Print.pm

#END DEPEND--------------------------------------------------------------------

perl <<'END_SCRIPT'
use strict;
use warnings;
use COD::CIF::Tags::Print qw( pack_precision );
use COD::Precision qw( unpack_cif_number );

my @tests = (
    [ 100,   1 ],
    [ 100,  10 ],
    [ 100, 100 ],

    [ 100.1,   1 ],
    [ 100.1,  10 ],
    [ 100.1, 100 ],

    [ 100.1, 0.1   ],
    [ 100.1, 0.01  ],
    [ 100.1, 0.001 ],

    [ 100.1, 1     ],
    [ 100.1, 1.1   ],
    [ 100.1, 1.01  ],
    [ 100.1, 1.001 ],

    [ 0.1, 1     ],
    [ 0.1, 0.1   ],
    [ 0.1, 0.01  ],
    [ 0.1, 0.001 ],

    [ 0.01,  0.01 ],
    [ 0.001, 0.001 ],

    [ 1.23,   0.1 ],
    [ 1.234,  0.1 ],
    [ 1.2345, 0.1 ],
);

foreach (@tests) {
    printf "%s ± %s = %s\n", @$_, pack_precision( @$_ );
    my( $value, $precision ) = unpack_cif_number( pack_precision( @$_ ) );
    if( $value != $_->[0] || $precision != $_->[1] ) {
        printf "Roundtrip failed for %s ± %s\n", @$_;
    }
}
END_SCRIPT
