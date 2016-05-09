#--*-perl-*-------------------------------------------------------------
#$Author$
#$Date$
#$Revision$
#$URL$
#-----------------------------------------------------------------------
# Test dataset on various criteria to determine if it should be included in 
# the statistics.
#-----------------------------------------------------------------------

package COD::CIF::Data::ExcludeFromStatistics;

use strict;
use warnings;
use COD::CIF::Data::CODFlags qw(
    is_on_hold
    is_duplicate
    is_retracted
    is_disordered
    is_suboptimal
    has_errors
    has_warnings
);

require Exporter;
our @ISA = qw( Exporter );
our @EXPORT_OK = qw(
    exclude_from_statistics
);

sub exclude_from_statistics($$);

##
# Checks dataset against the given set of criteria and determines if the
# dataset is suitable to be used in statistics.
#
# @param $dataset
#       Dataset of a CIF file as generated by 'CIFParser' parser.
# @fitness_criteria
#       A hash reference to the keyword-value pair flags of criteria for the 
#       dataset to be tested against. Setting the flag to 0, turns on the 
#       coresponding criteria. Currently supported criteria with their 
#       default values:
#       $fitness_criteria = {
#           'duplicates'   => 1,
#           'disorder'     => 1,
#           'suboptimal'   => 1,
#           'on-hold'      => 1,
#           'retracted'    => 1,
#           'has_warnings' => 1,
#           'has_errors'   => 1
#       }
#
#       In the given example (default), all criteria are turned off.
# @return $status
#       Binary value of '0' or '1', the latter meaning that the provided 
#       data block did not satisfy the required criteria.
# @return $warning
#       A text string containing an explanation for the data block not
#       satisfying the criteria that can be used in error messages. An
#       empty string is returned if the $status is 0.
##
sub exclude_from_statistics($$)
{
    my ( $dataset, $fitness_criteria ) = @_;

    my @criteria = ( 'duplicates', 'disordered', 'suboptimal', 'on-hold',
                     'retracted', 'has_warnings', 'has_errors' );

    # all structures are included by default
    foreach (@criteria) {
        $fitness_criteria->{$_} = 1 if ! exists($fitness_criteria->{$_})
    }

    my $warning = "";
    my $status = 1;

    if( !$fitness_criteria->{'duplicates'} && is_duplicate( $dataset ) ) {
        $warning = "dataset is marked as duplicate and should not " .
                   "be used for statistics";
    } elsif ( !$fitness_criteria->{'retracted'} && is_retracted( $dataset ) ) {
        $warning = "dataset was retracted and should not " .
                   "be used for statistics";
    } elsif ( !$fitness_criteria->{'disordered'} &&
                                                is_disordered( $dataset ) ) {
        $warning = "dataset is disordered and should not " .
                   "be used for statistics";
    } elsif ( !$fitness_criteria->{'suboptimal'} &&
                                                is_suboptimal( $dataset ) ) {
        $warning = "dataset is marked as suboptimal and should not " .
                   "be used for statistics";
    } elsif ( !$fitness_criteria->{'has_warnings'} && 
                                                has_warnings( $dataset ) ) {
        $warning = "dataset processing generated warnings and it should not " .
                   "be used for statistics";
    } elsif ( !$fitness_criteria->{'has_errors'} && has_errors( $dataset ) ) {
        $warning = "dataset has errors and should not " .
                   "be used for statistics";
    } elsif ( !$fitness_criteria->{'on-hold'} && is_on_hold( $dataset ) ) {
        $warning = "dataset is on-hold and should not " .
                   "be used for statistics";
    } else {
        $status = 0;
    };

return ($status, $warning);
}

1;
