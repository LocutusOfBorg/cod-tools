#! /bin/sh

#BEGIN DEPEND------------------------------------------------------------------
INPUT_MODULES='src/lib/perl5/COD/CIF/Data/CODFlags.pm'
#END DEPEND--------------------------------------------------------------------

perl <<'END_SCRIPT'
#------------------------------------------------------------------------------
#$Author$
#$Date$ 
#$Revision$
#$URL$
#------------------------------------------------------------------------------
#*
#* Unit test for the COD::CIF::Data::CODFlags::has_error_flag_value subroutine.
#* Tests the way the subroutine behaves when the input data block contains
#* the '_cod_error_flag' data item with the requested flag values.
#**

use strict;
use warnings;

use COD::CIF::Data::CODFlags;

my $data_block_with_none =
{
    'name'   => 'cod_error_flag_none',
    'tags'   => [ '_cod_error_flag' ],
    'loops'  => [],
    'inloop' => {},
    'values' => { '_cod_error_flag' => [ 'none' ] },
    'precisions' => {},
    'types' => { '_cod_error_flag' => [ 'UQSTRING' ] },
};

my $data_block_with_warnings =
{
    'name'   => 'cod_error_flag_warnings',
    'tags'   => [ '_cod_error_flag' ],
    'loops'  => [],
    'inloop' => {},
    'values' => { '_cod_error_flag' => [ 'warnings' ] },
    'precisions' => {},
    'types' => { '_cod_error_flag' => [ 'UQSTRING' ] },
};

my $data_block_with_errors =
{
    'name'   => 'cod_error_flag_errors',
    'tags'   => [ '_cod_error_flag' ],
    'loops'  => [],
    'inloop' => {},
    'values' => { '_cod_error_flag' => [ 'errors' ] },
    'precisions' => {},
    'types' => { '_cod_error_flag' => [ 'UQSTRING' ] },
};

my $data_block_with_a_retraction =
{
    'name'   => 'cod_error_flag_retracted',
    'tags'   => [ '_cod_error_flag' ],
    'loops'  => [],
    'inloop' => {},
    'values' => { '_cod_error_flag' => [ 'retracted' ] },
    'precisions' => {},
    'types' => { '_cod_error_flag' => [ 'UQSTRING' ] },
};

my $data_block = $data_block_with_none;
if (COD::CIF::Data::CODFlags::has_error_flag_value($data_block, 'none')) {
    print 'Data block \'' . $data_block->{'name'} . '\' contains the \'none\' error flag.' . "\n";
} else {
    print 'Data block \'' . $data_block->{'name'} . '\' does not contain the \'none\' error flag.' . "\n";
}

$data_block = $data_block_with_warnings;
if (COD::CIF::Data::CODFlags::has_error_flag_value($data_block, 'warnings')) {
    print 'Data block \'' . $data_block->{'name'} . '\' contains the \'warnings\' error flag.' . "\n";
} else {
    print 'Data block \'' . $data_block->{'name'} . '\' does not contain the \'warnings\' error flag.' . "\n";
}

$data_block = $data_block_with_errors;
if (COD::CIF::Data::CODFlags::has_error_flag_value($data_block, 'errors')) {
    print 'Data block \'' . $data_block->{'name'} . '\' contains the \'errors\' error flag.' . "\n";
} else {
    print 'Data block \'' . $data_block->{'name'} . '\' does not contain the \'errors\' error flag.' . "\n";
}

$data_block = $data_block_with_a_retraction;
if (COD::CIF::Data::CODFlags::has_error_flag_value($data_block, 'retracted')) {
    print 'Data block \'' . $data_block->{'name'} . '\' contains the \'retracted\' error flag.' . "\n";
} else {
    print 'Data block \'' . $data_block->{'name'} . '\' does not contain the \'retracted\' error flag.' . "\n";
}

END_SCRIPT
