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
#* Unit test for the COD::CIF::Data::CODFlags::is_suboptimal subroutine.
#* Tests the way the subroutine behaves when the input data block contains
#* no data items that marks it as an suboptimal structure.
#**

use strict;
use warnings;

use COD::CIF::Data::CODFlags qw( is_suboptimal );

my $data_block_1 =
{
  'name'   => 'neutral_item',
  'tags'   => [ '_neutral_item' ],
  'loops'  => [ ],
  'inloop' => {},
  'values' => { '_neutral_item' => [ 'yes' ] },
  'precisions' => {},
  'types'  => { '_neutral_item' => [ 'UQSTRING' ] },
};

my @blocks = (
    $data_block_1,
);

for my $data_block ( @blocks ) {
    my $is_suboptimal = is_suboptimal( $data_block );
    if ( $is_suboptimal ) {
        print 'Data block \'' . $data_block->{'name'} . '\' is marked as suboptimal.' . "\n";
    } else {
        print 'Data block \'' . $data_block->{'name'} . '\' is not marked as suboptimal.' . "\n";
    }
}

END_SCRIPT
