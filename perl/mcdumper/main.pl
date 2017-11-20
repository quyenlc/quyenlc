#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;
use File::Basename;
use lib dirname (__FILE__);
use Cache::Memcached;


my $memcached_host = $ARGV[0];
my $memcached_port = $ARGV[1];

my $dest_host = $ARGV[2];
my $dest_port = $ARGV[3];
my $key_file = $ARGV[4];

my $memd;
my $now_ts = time();
my $expire_time = 0;

if ( $dest_port && $dest_port ) {
    $memd = new Cache::Memcached {
        'servers' => [ "$dest_host:$dest_port" ],
        'debug'   => 1,
    };
}

open( DATA, "+>/tmp/$memcached_host.txt" ) or die "Couldn't open file .txt, $!";
close( DATA );

sub insertkey {
    my ( $key_value ) = @_;
    open( DATA,">>/tmp/$memcached_host.txt" ) || die "Couldn't open file file.txt, $!";
    print DATA $key_value;
    close( DATA );
}

sub copykey {
    my ( $key, $expire_time ) = @_;
    if ( $key !~ 'AmazonElastiCache:cluster' ) {
        my @value_info = `echo "get $key" | nc $memcached_host $memcached_port`;
        my $value = '';

        if ( scalar @value_info > 2 ) {
            for (1..scalar @value_info - 2) {
                $value .= "$value_info[$_]";
            }

            $value = substr( $value, 0, -2 );
            insertkey("$key,$value,$expire_time\n");
            print "$key,$value,$expire_time\n";

            if ( $dest_port && $dest_port ) {
                if ( $memd->set( $key, $value, $expire_time ) ) {
                    print "Set key '$key' successfully\n";
                } else {
                    print "Set key '$key' unsuccessfully\n";
                }
            }
        } else {
            print "Key '$key' is empty\n";
        }
    }
}

if ( $key_file ){
    my @keylist = `cat $key_file`;

    for  my $key ( @keylist ) {
        chomp($key);
        copykey( $key, 0); # keys in file are never expire
    }
} else {
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
                    $expire_time = $data[4];

                    if ( $expire_time < $now_ts ) { # check if this key is expired (!)
                        $expire_time = 0;
                    }
                    copykey($key, $expire_time);
                }
            }
        }
    }
}
