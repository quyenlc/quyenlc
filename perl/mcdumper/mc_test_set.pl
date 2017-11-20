#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;
use File::Basename;
use lib dirname (__FILE__);
use Cache::Memcached;
my $memd = new Cache::Memcached {
    'servers' => [ "ult-n-cache-test.vduefj.0001.usw1.cache.amazonaws.com:11211" ],
    'debug' => 1,
    'compress_threshold' => 10_000,
};
my $now_ts = time();
print "\n$now_ts\n";
#Key: superraid_counter_2 - Size: 3 - Expire Time: 1427911445 - Value: |108|
#Cache::Memcache: set superraid_counter_3 = 174 (set superraid_counter_3 0 1427911445 3 174)
#$memd->set("superraid_counter_2", "108", 1427911445);
