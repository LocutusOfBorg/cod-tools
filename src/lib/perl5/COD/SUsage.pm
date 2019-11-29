#------------------------------------------------------------------------
#$Author$
#$Date$ 
#$Revision$
#$URL$
#------------------------------------------------------------------------
#*
#  Simple usage message generator.
#**

package COD::SUsage;

use strict;
use warnings;

require Exporter;
our @ISA = qw(Exporter);
our @EXPORT_OK = qw(
    options
    usage
);

sub usage
{
    my $script = shift;
    $script = $0 unless defined $script;

    open my $script_fh, $script or die "Could not open $script: $!";
    while( <$script_fh> ) {
        if( /^\s*#\*/ .. /^\s*#\*\*/ ) {
            /^\s*#\*?\*?/;
            my $line = "$'";
            $line =~ s/\$0/$0/g;
            print $line;
        }
    }
    close $script_fh;
}

sub options
{
    my $script = shift;
    $script = $0 unless defined $script;

    print "$script: The '--options' option is a placehoder.\n";
    print "$script: It should be replaced by one of the following options:\n";
    open my $script_fh, $0 or die $!;
    while( <$script_fh> ) {
        if( /^#\*\s+OPTIONS:/../^#\*\*/ ) {
            s/^#\*\s+OPTIONS://;
            s/^#\*\*?//;
            s/\$0/$0/g;
            print;
        }
    }
    close $script_fh;
}

1;
