#------------------------------------------------------------------------------
#$Author$
#$Date$
#$Revision$
#$URL$
#------------------------------------------------------------------------------
#*
#  Format run time error and warning messages in a uniform way.
#**

package COD::UserMessage;

use strict;
use warnings;
use List::Util qw( max );

require Exporter;
our @ISA = qw( Exporter );
our @EXPORT_OK = qw(
    print_message
    error
    warning
    note
    parse_message
    sprint_message
    debug_note
);

# characters that will be escaped as HTML5 entities
# TODO: an escape strategy that cover the entirety of symbols that are not
# allowed should be implemented
my %common_escape = ( '&' => '&amp;', ':' => '&colon;', "\n" => '&#10;', );
my %ws_escape     = ( ' ' => '&nbsp;', "\t" => '&Tab;', );

my %program_escape  = ( %common_escape,
                        '(' => '&lpar;',   ')' => '&rpar;',
                        '{' => '&lbrace;', '}' => '&rbrace;',
                        '[' => '&lbrack;', ']' => '&rbrack;', );
my %filename_escape = ( %program_escape, %ws_escape );
my %add_pos_escape  = ( %common_escape );
my %message_escape  = ( %common_escape );

#==============================================================================
# Construct an error message, reporting a program name, file name, data block
# name and the error level (i.e. ERROR) in a uniform way.

sub sprint_message
{
    my ( $message_details ) = @_;

    my $program      = $message_details->{'program'};
    my $filename     = $message_details->{'filename'};
    my $line_no      = $message_details->{'line_no'};
    my $column_no    = $message_details->{'column_no'};
    my $add_pos      = $message_details->{'add_pos'};
    my $err_level    = $message_details->{'err_level'};
    my $message      = $message_details->{'message'};
    my $line_content = $message_details->{'line_content'};

    $message =~ s/\.?\n?$//;

    #$program = "perl -e '...'" if ( $program eq '-e' );

    $program     = escape_meta( $program,     \%program_escape  );
    $filename    = escape_meta( $filename,    \%filename_escape );
    $add_pos     = escape_meta( $add_pos,     \%add_pos_escape  );
    $message     = escape_meta( $message,     \%message_escape  );

    $line_content = prefix_multiline($line_content);

    return $program . ':' .
           (defined $filename ? ' ' . $filename .
                (defined $line_no ? "($line_no" .
                    (defined $column_no ? ",$column_no" : '') . ')'
                : '') .
                (defined $add_pos ? " $add_pos" : '')
           : '') . ': ' .
           (defined $err_level ? $err_level . ', ' : '') .
           $message .
           (defined $line_content ? ":\n" . $line_content . "\n" .
                (defined $column_no ? ' ' . ' ' x max( 0, $column_no-1 ) . "^\n" : '')
                : ".\n");
}

#==============================================================================
# Generic function for printing messages to STDERR

sub print_message
{
    my ( $message_details ) = @_;
    print STDERR sprint_message( $message_details );

    return;
}

###
# Parses an error message based on the formal error message grammar [1].
# Error messages that adhere to the aforementioned grammar can be produced
# using the sprint_message() subroutine.
#
# @source [1]
#       "EBNF grammar", supporting information of [2].
#       doi: 10.1107/S1600576715022396/po5052sup2.txt
# @source [2]
#       Merkys, A., Vaitkus, A., Butkus, J., Okulič-Kazarinas, M.,
#       Kairys, V. & Gražulis, S. (2016). COD::CIF::Parser:
#       an error-correcting CIF parser for the Perl language.
#       Journal of Applied Crystallography, 49.
#       doi: 10.1107/S1600576715022396
# @param $message
#       Text string that contains the error message.
# @return
#       Reference to a hash that contains the parsed error message
#       or an undef value if the message could not be parsed.
#       The returned hash contains the following keys:
#       {
#         # Name of the program that issued the error
#           'program'   => 'cif_parse',
#         # Name of the file that caused the error
#           'filename'  => 'test.cif',
#         # Number of the line that caused the error
#           'line_no'   => 13,
#         # Number of the line column that caused the error
#           'column_no' => 27,
#         # Additional details about the location of the error
#           'add_pos'   => 'data_parser_test_1',
#         # Error level
#           'err_level' => 'ERROR',
#         # Message explaining the error
#           'message'   => 'incorrect CIF syntax',
#         # Lines that caused the error
#           'line_content' => "loop__\n" .
#                             "^\n"
#       }
#
#       All keys except for 'program' and 'message' may have
#       undef values.
###
sub parse_message($)
{
    my( $message ) = @_;

    my $file_name_char = qr/[^\x{00}-\x{20}():\[\]\{\}\x{7F}]/;
    my $program   = qr/$file_name_char(?:$file_name_char|[ \t])*/;
    my $file_name = qr/$file_name_char+/;
    my $err_level = qr/[A-Z][A-Z_0-9 -]*/ms;
    if( $message =~ /^
             ($program):[ ]?
             (?:
                 ($file_name)
                     (?: \( ([0-9]+) (?:,([0-9]+))? \) )?
                     (?: [ ]([^:]+?) )?
             )?
             :[ ]?
             (?: ($err_level)[,][ ])?
             (?:([^\n:]+?)(?:\.?\n?)?)
             (?: \: \s* \n
                 (
                 (?: [ ][^\n]*\n )*
                 )
             )?
         $/msxg ) {
        return {
            program      => unescape_meta($1, \%program_escape),
            filename     => unescape_meta($2, \%filename_escape),
            line_no      => $3,
            column_no    => $4,
            add_pos      => unescape_meta($5, \%add_pos_escape),
            err_level    => $6,
            message      => unescape_meta($7, \%message_escape),
            line_content => unprefix_multiline($8)
        };
    }

    return;
}

#==============================================================================
# Report an error message. Errors are indicated with the "ERROR"
# keyword in the message line. This is supposed to be a fatal event,
# and the program will most probably die() or exit(255) after this
# message, but the UserMessage package does not enforce this policy.

sub error
{
    my ( $message_details ) = @_;
    print_message( {
        'err_level' => 'ERROR',
        'program'   => $message_details->{'program'},
        'filename'  => $message_details->{'filename'},
        'add_pos'   => $message_details->{'add_pos'},
        'message'   => $message_details->{'message'}
    } );

    return;
}

#==============================================================================
# Report a warning message. Warnings are indicated with the "WARNING"
# keyword. Program can probably continue after warnings and give a
# reasonable result, but it might not be the result which the user
# expected.

sub warning
{
    my ( $message_details ) = @_;
    print_message( {
        'err_level' => 'WARNING',
        'program'   => $message_details->{'program'},
        'filename'  => $message_details->{'filename'},
        'add_pos'   => $message_details->{'add_pos'},
        'message'   => $message_details->{'message'}
    } );

    return;
}

#==============================================================================
# Report a note message. Notes are indicated with the "NOTE"
# keyword. Program can always continue after issuing notes as the intent
# of note is to just provide information on the progress.

sub note
{
    my ( $message_details ) = @_;
    print_message( {
        'err_level' => 'NOTE',
        'program'   => $message_details->{'program'},
        'filename'  => $message_details->{'filename'},
        'add_pos'   => $message_details->{'add_pos'},
        'message'   => $message_details->{'message'}
    } );

    return;
}

#==============================================================================
# Report a debug message. Notes are indicated with the "DEBUG"
# keyword. Debug messages should only be printed upon user request to output
# additional information.

sub debug_note
{
    my ( $message_details ) = @_;
    print_message( {
        'err_level' => 'DEBUG',
        'program'   => $message_details->{'program'},
        'filename'  => $message_details->{'filename'},
        'add_pos'   => $message_details->{'add_pos'},
        'message'   => $message_details->{'message'}
    } );

    return;
}

sub escape_meta {
    my ( $text, $escaped_symbols ) = @_;

    return undef if !defined $text;

    my $symbols = join '|', map { '\\' . $_ } keys %{$escaped_symbols};

    $text =~ s/($symbols)/$escaped_symbols->{"$1"}/g;

    return $text;
}

sub unescape_meta {
    my ( $text, $escaped_symbols ) = @_;

    return undef if !defined $text;

    my %unescaped_symbols = reverse %{$escaped_symbols};

    my $symbols = join '|', keys %unescaped_symbols;

    $text =~ s/($symbols)/$unescaped_symbols{"$1"}/g;

    return $text;
}

sub prefix_multiline
{
    my ($multiline) = @_;

    if( defined $multiline ) {
        # Empty line has to be dealt separately, as split'ting empty
        # line returns empty array:
        if( $multiline ne '' ) {
            $multiline = join( "\n", map { " $_" }
                                         split( "\n", $multiline ) );
        } else {
            $multiline = ' ';
        }
    }

    return $multiline;
}

sub unprefix_multiline
{
    my ($multiline) = @_;

    $multiline =~ s/^ //msg if defined $multiline;

    return $multiline;
}

1;
