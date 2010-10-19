#! /bin/sh
#!perl -w # --*- Perl -*--
eval 'exec perl -x $0 ${1+"$@"}'
    if 0;
#------------------------------------------------------------------------------
#$Author$
#$Date$
#$Revision$
#$URL$
#------------------------------------------------------------------------------
#*
#  Find COD numbers for the .cif files in given directories of file lists.
#
#  Usage:
#      find-numbers.pl my-cif-dir1/ my-cif-dir2/files*.cif  COD-cif-dir/ 
#**

use strict;
use File::Basename;

my $check_bibliography = 1;

my $max_cell_length_diff = 0.5; # Angstroems
my $max_cell_angle_diff  = 1.2; # degrees

my %has_numeric_value = (
    "_journal_year"   => 1,
    "_journal_volume" => 1,
    "_journal_issue"  => 1,
);

my %skip_tag = (
    "_journal_name_full" => 0,
);

my %COD = ();

if( @ARGV < 2 ) {
    print STDERR "$0: please supply two directory names on the command line:\n";
    print STDERR "first directory with the analysed CIF files,\n";
    print STDERR "and the second with the COD CIF files.\n";
    exit -1;
}

my $COD_cif_dir = pop( @ARGV );
my @COD_cif_files = `find $COD_cif_dir -name "*.cif" -o -name "*.CIF"`;

do {
    print int(@COD_cif_files), "\n";
    print "@COD_cif_files";
} if 0;

for my $file (@COD_cif_files) {

    chomp $file;
    open( CODCIF, "<$file" ) or
        die( "$0: could not open file '$file' for reading: $!" );

    my %structures = ();
    my $id;

    while( <CODCIF> ) {
        if( /^\s*data_(.*)/ ) {
            $id = $1;
            $structures{$id}{id} = $id;
            $structures{$id}{filename} = File::Basename::basename( $file );
        }
        if( /^\s*_chemical_formula_sum\s+(.*)/ ) {
            my $formula = $1;
            $formula =~ s/^\s*'\s*|\s*'\s*$//g;
            $formula =~ s/\s+/ /g;
            my $sorted = join( " ", sort {$a cmp $b} split( " ", $formula ));
            $structures{$id}{chemical_formula_sum} = $sorted;
        }
        if( /^\s*(_cell_(?:length_a|length_b|length_c|
                     angle_alpha|angle_beta|angle_gamma))\s+([\d.]+)/x ) {
            my $key = $1;
            my $val = $2;
            $val =~ s/^\s*'\s*|\s*'\s*$//g;
            $val =~ s/\(.*$//;
            $val =~ s/[()_a-zA-Z]//g;
            $structures{$id}{cell}{$key} = sprintf "%f", $val;
        }
        if( /^\s*(_[^\s]*temperature[^\s]*)\s+(.*)/ ) {
            $structures{$id}{temperature}{$1} = $2;
            $structures{$id}{temperature}{$1} =~ s/^\s*'\s*|\s*'\s*$//g;
        }
        if( /^\s*(_[^\s]*pressure[^\s]*)\s+(.*)/ ) {
            $structures{$id}{pressure}{$1} = $2;
            $structures{$id}{pressure}{$1} =~ s/^\s*'\s*|\s*'\s*$//g;
        }
        if( /^\s*(_journal_[^\s]*)\s+(.*)\s*$/ && 
            ! /^\s*_journal_name/ ) {
            my $key = $1;
            my $value = $2;
            $value =~ s/^['"]|["']$//g;
            $structures{$id}{bibliography}{$key} = $value;
        }
        if( /^\s*(_\[local\])?_cod_suboptimal_structure\s+(.*)\s*$/ ) {
            ## print ">>>>>> $2\n";
            $structures{$id}{suboptimal} = $2;
        }
    }

    close( CODCIF );

    my $basename = File::Basename::basename( $file );
    for my $id (keys %structures) {
        my $formula = $structures{$id}{chemical_formula_sum};

        $formula = '?' unless defined $formula;

        push( @{$COD{$formula}}, $structures{$id} );
    }
}

do {
    use Serialise;
    serialiseRef( \%COD );
} if 0;

#------------------------------------------------------------------------------

my @cif_files = `find @ARGV -name "*.cif" -o -name "*.CIF"`;

for my $file (@cif_files) {
    chomp $file;
    open( CIF, "<$file" ) or
        die( "$0: could not open file '$file' for reading: $!" );

    my %structures = ();
    my $id;

    while( <CIF> ) {
        if( /^\s*data_(.*)/ ) {
            $id = $1;
            $structures{$id}{id} = $id;
            $structures{$id}{filename} = File::Basename::basename( $file );
        }
        if( /^\s*_chemical_formula_sum\s+(.*)/ ) {
            my $formula = $1;
            $formula =~ s/^\s*'\s*|\s*'\s*$//g;
            $formula =~ s/\s+/ /g;
            my $sorted = join( " ", sort {$a cmp $b} split( " ", $formula ));
            $structures{$id}{chemical_formula_sum} = $sorted;
        }
        if( /^\s*(_cell_(?:length_a|length_b|length_c|
                     angle_alpha|angle_beta|angle_gamma))\s+([\d.]+)/x ) {
            my $key = $1;
            my $val = $2;
            $val =~ s/^\s*'\s*|\s*'\s*$//g;
            $val =~ s/\(.*$//;
            $structures{$id}{cell}{$key} = sprintf "%f", $val;
        }
        if( /^\s*(_[^\s]*temperature[^\s]*)\s+(.*)/ ) {
            $structures{$id}{temperature}{$1} = $2;
            $structures{$id}{temperature}{$1} =~ s/^\s*'\s*|\s*'\s*$//g;
        }
        if( /^\s*(_[^\s]*pressure[^\s]*)\s+(.*)/ ) {
            $structures{$id}{pressure}{$1} = $2;
            $structures{$id}{pressure}{$1} =~ s/^\s*'\s*|\s*'\s*$//g;
        }
        if( /^\s*(_journal_[^\s]*)\s+(.*)\s*$/ && 
            ! /^\s*_journal_name/ ) {
            my $key = $1;
            my $value = $2;
            $value =~ s/^['"]|["']$//g;
            $structures{$id}{bibliography}{$key} = $value;
        }
        if( /^\s*(_\[local\])?_cod_suboptimal_structure\s+(.*)\s*$/ ) {
            ## print ">>>>>> $2\n";
            $structures{$id}{suboptimal} = $2;
        }
    }

    for $id (keys %structures) {
        my $formula = $structures{$id}{chemical_formula_sum};

        $formula = '?' unless defined $formula;

        my $final_formula = $formula;
        $final_formula =~ s/\s/_/g;

        my $n = 0;
        if( defined $COD{$formula} ) {
            for my $COD_entry (@{$COD{$formula}}) {
                if( entries_are_the_same( $structures{$id}, $COD_entry )) {
                    $n++;
                }
            }
        }
        if( $n > 0 ) {
            for my $COD_entry (@{$COD{$formula}}) {
                if( entries_are_the_same( $structures{$id}, $COD_entry )) {
                    printf
                        "%-35s %15s %3d %s\n",
                        $final_formula, 
                        $COD_entry->{filename}, $n, $file;
                }
            }
        } else {
            printf "%-35s %15s %3d %s\n", $final_formula, "?", 0, $file;
        }
    }

    close( CIF );
}

#------------------------------------------------------------------------------

sub get_cell($)
{
    my $datablok = $_[0];

    return (
        $datablok->{_cell_length_a},
        $datablok->{_cell_length_b},
        $datablok->{_cell_length_c},
        $datablok->{_cell_angle_alpha},
        $datablok->{_cell_angle_beta},
        $datablok->{_cell_angle_gamma}
    );
}

sub cells_are_the_same($$)
{
    my ($cell1, $cell2) = @_;

    my @cell1 = get_cell( $cell1 );
    my @cell2 = get_cell( $cell2 );

    my $max_length_diff = 0;
    my $max_angle_diff = 0;

    for my $i (0..2) {
        my $length1 = $cell1[$i];
        my $length2 = $cell2[$i];
        if( defined $length1 and defined $length2 ) {
            my $diff = abs( $length1 - $length2 );
            if( $max_length_diff < $diff ) {
                $max_length_diff = $diff;
            }
        }
    }
    for my $i (3..5) {
        my $angle1 = $cell1[$i];
        my $angle2 = $cell2[$i];
        if( defined $angle1 and defined $angle2 ) {
            my $diff = abs( $angle1 - $angle2 );
            if( $max_angle_diff < $diff ) {
                $max_angle_diff = $diff;
            }
        }
    }

    return
        $max_length_diff < $max_cell_length_diff &&
        $max_angle_diff < $max_cell_angle_diff;
}

sub conditions_are_the_same
{
    my ($entry1, $entry2) = @_;

    for my $parameter ("temperature", "pressure" ) {

        my %tags = map {($_,$_)} ( keys %{$entry1->{$parameter}},
                                   keys %{$entry2->{$parameter}} );
        for my $tag (keys %tags) {
            if( exists $entry1->{$parameter}{$tag} &&
                exists $entry2->{$parameter}{$tag} &&
                $entry1->{$parameter}{$tag} ne $entry2->{$parameter}{$tag} ) {
                return 0;
            }
        }
    }
    return 1;
}

sub bibliographies_are_the_same($$)
{
    my ($biblio1, $biblio2) = @_;

    my %tags = map {($_,$_)} ( keys %$biblio1, keys %$biblio2 );

    for my $tag ( keys %tags ) {
        next if( $skip_tag{$tag} );
        if( defined $biblio1->{$tag} && defined $biblio2->{$tag} ) {
            if( $has_numeric_value{$tag} ) {
                if( $biblio1->{$tag} != $biblio2->{$tag} ) {
                    return 0;
                }
            } else {
                if( $biblio1->{$tag} ne $biblio2->{$tag} ) {
                    return 0;
                }
            }
        }
    }
    return 1;
}

sub data_sections_are_the_same($$)
{
    my ($entry1, $entry2) = @_;

    return
        $entry1->{filename} eq $entry2->{filename} &&
        $entry1->{id} eq $entry2->{id};
}

sub entries_are_the_same
{
    my ($entry1, $entry2) = @_;
    
    ## print ">>> $entry1->{id}, $entry2->{id}, ",
    ## defined $entry1->{suboptimal} ? $entry1->{suboptimal} : "" , " ", 
    ## defined $entry2->{suboptimal} ? $entry2->{suboptimal} : "", "\n";

    if( $check_bibliography ) {
        return
            ! data_sections_are_the_same( $entry1, $entry2 ) &&
            cells_are_the_same( $entry1->{cell}, $entry2->{cell} ) &&
            conditions_are_the_same( $entry1, $entry2 ) &&
            (!defined $entry1->{suboptimal} || $entry1->{suboptimal} ne "yes") &&
            (!defined $entry2->{suboptimal} || $entry2->{suboptimal} ne "yes") &&
            bibliographies_are_the_same( $entry1->{bibliography},
                                         $entry2->{bibliography} );
    } else {
        return
            ! data_sections_are_the_same( $entry1, $entry2 ) &&
            conditions_are_the_same( $entry1, $entry2 ) &&
            (!defined $entry1->{suboptimal} || $entry1->{suboptimal} ne "yes") &&
            (!defined $entry2->{suboptimal} || $entry2->{suboptimal} ne "yes") &&
            cells_are_the_same( $entry1->{cell}, $entry2->{cell} );
    }
}

## sub cell_volume
## {
##     my @cell = @_;
## 
##     if( !defined $cell[0] || !defined $cell[1] || !defined $cell[2] ||
##         !defined $cell[3] || !defined $cell[4] || !defined $cell[5] ) {
##         return -1;
##     }
## 
##     my $Pi = 3.14159265358979;
## 
##     @cell = map { s/\(.*\)//g; $_ } @_;
## 
##     my ($a, $b, $c) = @cell[0..2];
##     my ($alpha, $beta, $gamma) = map {$Pi * $_ / 180} @cell[3..5];
##     my ($ca, $cb, $cg) = map {cos} ($alpha, $beta, $gamma);
##     my $sg = sin($gamma);
##     
##     my $V = $a * $b * $c * sqrt( $sg**2 - $ca**2 - $cb**2 + 2*$ca*$cb*$cg );
## 
##     return $V;
## }
## 
## sub compute_datablock_cell_volume
## {
##     my $values = $_[0];
##     my @cell = get_cell( $values );
##     return cell_volume( @cell );
## }
