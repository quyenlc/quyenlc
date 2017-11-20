#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;
use File::Basename;
use lib dirname (__FILE__);
use Cache::Memcached;

my $memcached_host = $ARGV[0];
my $memcached_port = $ARGV[1];
my $now_ts = time();
open( DATA, "+>/tmp/$memcached_host-never-expire.txt" ) or die "Couldn't open file .txt, $!";
close( DATA );
sub insertkey {
    my ( $key_value ) = @_;
    open( DATA,">>/tmp/$memcached_host-never-expire.txt" ) || die "Couldn't open file file.txt, $!";
    print DATA $key_value;
    close( DATA );
}

my @cmd_output = `echo "stats items" | nc $memcached_host $memcached_port`;
for my $row (@cmd_output) {
        if ( $row =~ /items:\d+:number/ ) { # "STAT items:1:number 8"
            my @mc_info = split(/\s+/, $row);
            my @slab_info = split(/:+/, $mc_info[1]); # "items:1:number"
            my $slab = $slab_info[1];
            my @cmd_output1 = `echo "stats cachedump $slab 0" | nc $memcached_host $memcached_port`;

            for my $row1 (@cmd_output1) {
                if ( $row1 =~ /^ITEM/ ) { # "ITEM superraid_counter_1 [3 b; 1427911445 s]"
                    my @data = split(/\s+/, $row1);
                    my $key = $data[1];
                    my $expire_time = $data[4];

                    if ( $expire_time < $now_ts ) { # check if this key is expired (!)
                        my @value_info = `echo "get $key" | nc $memcached_host $memcached_port`;
                        if ( scalar @value_info > 2 ) {
                            print "$key\n";
                        }
                    }
                }
            }
        }
    }
