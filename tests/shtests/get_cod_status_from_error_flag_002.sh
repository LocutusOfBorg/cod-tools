#! /bin/sh

#BEGIN DEPEND------------------------------------------------------------------
INPUT_MODULES='src/lib/perl5/COD/CIF/Data/CIF2COD.pm'
#END DEPEND--------------------------------------------------------------------

perl <<'END_SCRIPT'
#------------------------------------------------------------------------------
#$Author$
#$Date$ 
#$Revision$
#$URL$
#------------------------------------------------------------------------------
#*
#* Unit test for the COD::CIF::Data::CIF2COD::get_cod_status_from_error_flag
#* subroutine. Tests the way the subroutine behaves when the input data block
#* contains the '_[local]_cod_error_flag' data item with various flag values.
#**

use strict;
use warnings;

use COD::CIF::Data::CIF2COD;

my $data_block =
{
    'name'   => '[local]_cod_error_flag',
    'tags'   => [ '_[local]_cod_error_flag' ],
    'loops'  => [],
    'inloop' => {},
    'values' => { '_[local]_cod_error_flag' => [ 'warnings' ] },
    'precisions' => {},
    'types' => { '_[local]_cod_error_flag' => [ 'UQSTRING' ] },
};

my $value = COD::CIF::Data::CIF2COD::get_cod_status_from_error_flag($data_block);
if (defined $value) {
    print 'Data block \'' . $data_block->{'name'} . "' has the '$value' status." . "\n";
} else {
    print 'Data block \'' . $data_block->{'name'} . '\' has an undefined status.' . "\n";
}

$data_block->{'values'}{'_[local]_cod_error_flag'}[0] = 'errors';
$value = COD::CIF::Data::CIF2COD::get_cod_status_from_error_flag($data_block);
if (defined $value) {
    print 'Data block \'' . $data_block->{'name'} . "' has the '$value' status." . "\n";
} else {
    print 'Data block \'' . $data_block->{'name'} . '\' has an undefined status.' . "\n";
}

$data_block->{'values'}{'_[local]_cod_error_flag'}[0] = 'retracted';
$value = COD::CIF::Data::CIF2COD::get_cod_status_from_error_flag($data_block);
if (defined $value) {
    print 'Data block \'' . $data_block->{'name'} . "' has the '$value' status." . "\n";
} else {
    print 'Data block \'' . $data_block->{'name'} . '\' has an undefined status.' . "\n";
}

# Data item contains a value that is allowed by the DDL1 dictionary,
# but not by the SQL schema 
$data_block->{'values'}{'_[local]_cod_error_flag'}[0] = 'none';
$value = COD::CIF::Data::CIF2COD::get_cod_status_from_error_flag($data_block);
if (defined $value) {
    print 'Data block \'' . $data_block->{'name'} . "' has the '$value' status." . "\n";
} else {
    print 'Data block \'' . $data_block->{'name'} . '\' has an undefined status.' . "\n";
}

# Data item contains a value that is allowed neither by the DDL1 dictionary,
# nor by the SQL schema
$data_block->{'values'}{'_[local]_cod_error_flag'}[0] = 'unknown';
$value = COD::CIF::Data::CIF2COD::get_cod_status_from_error_flag($data_block);
if (defined $value) {
    print 'Data block \'' . $data_block->{'name'} . "' has the '$value' status." . "\n";
} else {
    print 'Data block \'' . $data_block->{'name'} . '\' has an undefined status.' . "\n";
}

END_SCRIPT
