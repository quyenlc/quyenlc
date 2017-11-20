#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;
use File::Basename;
use lib dirname (__FILE__);
my ( $list_file ) = @ARGV;
my @table_list = `cat $list_file`;
sub in_list {
    my ( $file_name ) = @_;
    my $table_name = substr($file_name, 11, -7);
    for my $iline (@table_list) {
        chomp($iline);
        if ( $iline eq $table_name ) {
            return 1;
        }
    }
    return 0;
}
my @file_list = `ls |grep "sql.gz"`;
for my $line (@file_list) {
    chomp ($line);
    if ( in_list($line) ) {
        print "Table $line can be dropped\n";
    }
}