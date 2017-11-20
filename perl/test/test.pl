#!/user/sbin/perl
use strict;
use warnings;

my @az = ( qw| us-west-1a us-west-1c| );
my @sorted_idc = sort @az;
for (my $j = 0; $j < @sorted_idc - 1; $j += 1) {
    print "J: $sorted_idc[$j]\n";    
}

print "---End---\n";
